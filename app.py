"""The capstone web app.

You should not need to change this file. It is the same for every student.
Your project is the folder that config.py points to:

    projects/my_project/settings.py   names, labels, and the Add form
    projects/my_project/schema.sql    CREATE TABLE statements
    projects/my_project/seed.sql      INSERT statements with sample rows
    projects/my_project/queries/      one SQL file for each page

Run it in VS Code with the Run button at the top right of this file, or in
the terminal with:   python app.py
Then open http://127.0.0.1:5000 in your browser. Stop it with Ctrl + C.
"""

import os

from flask import Flask, flash, redirect, render_template, request, url_for

import config
from database import NotWritten, Project, SqlProblem

app = Flask(__name__)
# Only used to sign the short "Added" messages. Nothing secret is stored.
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24).hex()

app.jinja_env.globals.update(zip=zip, dict=dict)

project = Project(config.PROJECT_FOLDER)
project.build_database()


@app.context_processor
def site_settings():
    return {"site": project.settings, "project": project,
            "build_problem": project.build_problem}


def attempt(relative, params=None):
    """Runs a query file for a page. Returns (result, problem): the problem
    is a NotWritten or SqlProblem for the page to explain, else None."""
    if project.build_problem:
        return None, project.build_problem
    try:
        return project.query(relative, params), None
    except (NotWritten, SqlProblem) as e:
        return None, e


def id_column(result):
    """The column named id (any capitalization), used for links."""
    if not result:
        return None
    for name in result.columns:
        if name.lower() == "id":
            return name
    return None


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    stats, problem = attempt("queries/stats.sql")
    return render_template("home.html", stats=stats.first() if stats else None, problem=problem)


@app.route("/browse")
def browse():
    result, problem = attempt("queries/list.sql")
    return render_template("browse.html", result=result, problem=problem, id_col=id_column(result))


@app.route("/item/<int:item_id>")
def detail(item_id):
    item, problem = attempt("queries/detail.sql", {"id": item_id})
    related, related_problem = (None, None)
    if item and item.rows:
        related, related_problem = attempt("queries/detail_related.sql", {"id": item_id})
    found = bool(item and item.rows)
    # Every column except id. The first one is the page heading.
    fields = [(k, v) for k, v in item.first().items() if k.lower() != "id"] if found else []
    heading = str(fields[0][1]) if fields else project.settings.get("ITEM", "item").capitalize()
    return render_template("detail.html", item=found, found=found, fields=fields, heading=heading,
                           problem=problem, related=related, related_problem=related_problem,
                           item_id=item_id), (200 if found or problem else 404)


@app.route("/search")
def search():
    term = request.args.get("q", "").strip()
    result, problem = (None, None)
    if term:
        result, problem = attempt("queries/search.sql", {"term": term})
    return render_template("search.html", term=term, result=result, problem=problem,
                           id_col=id_column(result))


@app.route("/report")
def report():
    result, problem = attempt("queries/report.sql")
    bar_max = None
    if result and result.rows and result.columns:
        last = [row[-1] for row in result.rows]
        if all(isinstance(v, (int, float)) for v in last if v is not None):
            bar_max = max((v for v in last if v is not None), default=0) or None
    return render_template("report.html", result=result, problem=problem, bar_max=bar_max)


def _form_options():
    """Dropdown choices for every select field on the Add form."""
    options, problem = {}, None
    for field in project.settings.get("ADD_FORM", []):
        if field.get("type") == "select":
            result, problem = attempt(field["options"])
            if problem:
                return {}, problem
            options[field["name"]] = result.rows
    return options, problem


def _read_form(fields):
    """The submitted values, converted to the right type, plus any errors."""
    values, errors = {}, []
    for field in fields:
        raw = request.form.get(field["name"], "").strip()
        label = field.get("label", field["name"])
        if not raw:
            if field.get("required"):
                errors.append(f"{label} is required.")
            values[field["name"]] = None
            continue
        if field.get("type") in ("number", "select"):
            try:
                number = float(raw)
                values[field["name"]] = int(number) if number.is_integer() else number
            except ValueError:
                errors.append(f"{label} must be a number.")
                values[field["name"]] = None
        else:
            values[field["name"]] = raw
    return values, errors


@app.route("/add", methods=["GET", "POST"])
def add():
    fields = project.settings.get("ADD_FORM", [])
    options, problem = _form_options()
    if not problem and not project.build_problem:
        try:
            project.read("queries/add.sql")
        except NotWritten as e:
            problem = e
    problem = project.build_problem or problem
    errors, values = [], {}
    if request.method == "POST" and not problem:
        values, errors = _read_form(fields)
        if not errors:
            try:
                project.change("queries/add.sql", values)
                flash("Added. Rows added on the website are temporary and reset when the app restarts.", "success")
                return redirect(url_for("browse"))
            except (NotWritten, SqlProblem) as e:
                errors.append(f"The database refused it: {getattr(e, 'message', e)}")
    return render_template("add.html", fields=fields, options=options, problem=problem,
                           errors=errors, values=request.form if request.method == "POST" else {})


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


if __name__ == "__main__":
    # extra_files makes the app restart (and rebuild the database) whenever
    # you save one of your SQL files.
    app.run(debug=True, extra_files=project.sql_files())
