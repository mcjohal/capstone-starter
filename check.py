"""Checks your project against the capstone requirements.

Run it in the VS Code terminal:

    python check.py

It builds a fresh copy of your database in memory (your real one is not
touched), runs every SQL file, and prints what is done, what is missing,
and what has a mistake. Run it as often as you like.

To check the library example instead:   python check.py library_example
"""

import sqlite3
import sys

import config
from database import NotWritten, Project, SqlProblem, friendly

# The requirements. Your instructor may change these numbers.
MIN_TABLES = 3
MIN_FOREIGN_KEYS = 2
MIN_ROWS_PER_TABLE = 10

PASS, TODO, FAIL = "PASS", "TODO", "FAIL"
results = []


def report(status, text, hint=None):
    results.append(status)
    print(f"  [{status}] {text}")
    if hint:
        print(f"         {hint}")


def run(conn, project, relative, params=None):
    sql = project.read(relative)
    try:
        cursor = conn.execute(sql, params or {})
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise SqlProblem(project.display_path(relative), friendly(e))
    columns = [d[0] for d in cursor.description] if cursor.description else []
    return columns, cursor.fetchall()


def check_query(conn, project, relative, label, params=None, need_id=False, one_row=False):
    try:
        columns, rows = run(conn, project, relative, params)
    except NotWritten:
        report(TODO, f"{label}: {relative} is not written yet")
        return None
    except SqlProblem as e:
        report(FAIL, f"{label}: {relative} has an error", e.message)
        return None
    if need_id and not any(c.lower() == "id" for c in columns):
        report(FAIL, f"{label}: {relative} needs a column named id",
               "For example:  SELECT book_id AS id, title AS \"Title\" ...")
        return columns, rows
    if not rows:
        report(FAIL, f"{label}: {relative} runs but returns no rows",
               "Check the WHERE clause, and that seed.sql has matching rows.")
        return columns, rows
    if one_row and len(rows) != 1:
        report(FAIL, f"{label}: {relative} should return 1 row but returned {len(rows)}",
               "Check the WHERE clause.")
        return columns, rows
    report(PASS, f"{label}: {relative} returns {len(rows)} row{'s' if len(rows) != 1 else ''}")
    return columns, rows


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else config.PROJECT_FOLDER
    project = Project(name)
    s = project.settings
    print(f"\nChecking projects/{name}\n")

    # -- settings ------------------------------------------------------------
    print("Settings (settings.py)")
    if s.get("SITE_NAME") in ("", "My Capstone Project") or s.get("YOUR_NAME") in ("", "Your Name"):
        report(TODO, "Fill in SITE_NAME, TAGLINE, and YOUR_NAME in settings.py")
    else:
        report(PASS, f"Site name is {s['SITE_NAME']}, by {s['YOUR_NAME']}")

    # -- tables and rows -----------------------------------------------------
    print("\nTables (schema.sql) and rows (seed.sql)")
    conn = sqlite3.connect(":memory:")
    try:
        project.load_into(conn)
    except NotWritten as e:
        report(TODO, f"{e.path} is not written yet")
    except SqlProblem as e:
        line = f", statement starting on line {e.line}" if e.line else ""
        report(FAIL, f"{e.path}{line} has an error", e.message)
        print("\nFix that first: nothing else can be checked until schema.sql and seed.sql run.\n")
        return finish()

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    if not tables:
        print("\nWrite schema.sql first, then run this again.\n")
        return finish()

    status = PASS if len(tables) >= MIN_TABLES else FAIL
    report(status, f"{len(tables)} tables: {', '.join(tables)} (need at least {MIN_TABLES})")

    fk_total = 0
    for table in tables:
        info = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
        if not any(col[5] for col in info):
            report(FAIL, f"{table} has no primary key", f"Add a column like  {table}_id INTEGER PRIMARY KEY")
        fk_total += len(conn.execute(f'PRAGMA foreign_key_list("{table}")').fetchall())
    status = PASS if fk_total >= MIN_FOREIGN_KEYS else FAIL
    report(status, f"{fk_total} foreign keys (need at least {MIN_FOREIGN_KEYS})",
           None if status == PASS else "Add  FOREIGN KEY (column) REFERENCES other_table(column)")

    for table in tables:
        count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        if count >= MIN_ROWS_PER_TABLE:
            report(PASS, f"{table} has {count} rows")
        elif count == 0:
            report(TODO, f"{table} has no rows yet (need at least {MIN_ROWS_PER_TABLE})")
        else:
            report(FAIL, f"{table} has {count} rows (need at least {MIN_ROWS_PER_TABLE})")

    bad_links = conn.execute("PRAGMA foreign_key_check").fetchall()
    if bad_links:
        report(FAIL, f"{len(bad_links)} rows have a foreign key that points at a missing row",
               f"First one: table {bad_links[0][0]}, row {bad_links[0][1]}")

    # -- the pages -------------------------------------------------------------
    print("\nPages (the queries folder)")
    check_query(conn, project, "queries/stats.sql", "Home", one_row=True)
    listed = check_query(conn, project, "queries/list.sql", "Browse", need_id=True)

    sample_id = None
    if listed and listed[1]:
        id_index = next((i for i, c in enumerate(listed[0]) if c.lower() == "id"), None)
        if id_index is not None:
            sample_id = listed[1][0][id_index]
    if sample_id is None:
        report(TODO, "Detail: checked after list.sql works")
    else:
        check_query(conn, project, "queries/detail.sql", f"Detail (id {sample_id})", {"id": sample_id}, one_row=True)
        try:
            columns, rows = run(conn, project, "queries/detail_related.sql", {"id": sample_id})
            report(PASS, f"Detail related rows: queries/detail_related.sql returns {len(rows)} row{'s' if len(rows) != 1 else ''} for id {sample_id}")
        except NotWritten:
            report(TODO, "Detail related rows: queries/detail_related.sql is not written yet")
        except SqlProblem as e:
            report(FAIL, "Detail related rows: queries/detail_related.sql has an error", e.message)

    check_search(conn, project)
    check_query(conn, project, "queries/report.sql", "Report")
    check_add(conn, project)

    # -- CIS 4720 ------------------------------------------------------------------
    print("\nCIS 4720 only (schema.sql)")
    views = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'view'")]
    triggers = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")]
    report(PASS if views else TODO, f"Views: {', '.join(views) or 'none yet'}")
    report(PASS if triggers else TODO, f"Triggers: {', '.join(triggers) or 'none yet'}")

    return finish()


def check_search(conn, project):
    """Tries a few common letters, since the right word depends on your data."""
    for term in ("a", "e", "o", "1"):
        try:
            columns, rows = run(conn, project, "queries/search.sql", {"term": term})
        except NotWritten:
            return report(TODO, "Search: queries/search.sql is not written yet")
        except SqlProblem as e:
            return report(FAIL, "Search: queries/search.sql has an error", e.message)
        if not any(c.lower() == "id" for c in columns):
            return report(FAIL, "Search: queries/search.sql needs a column named id")
        if rows:
            return report(PASS, f"Search: searching for '{term}' finds {len(rows)} rows")
    report(FAIL, "Search: queries/search.sql never finds anything",
           "Use  LIKE '%' || :term || '%'  so the words can appear anywhere.")


def check_add(conn, project):
    fields = project.settings.get("ADD_FORM", [])
    if not fields:
        return report(TODO, "Add: ADD_FORM in settings.py is empty")
    sample = {}
    for field in fields:
        kind = field.get("type", "text")
        if kind == "select":
            try:
                columns, rows = run(conn, project, field["options"], {})
            except NotWritten:
                return report(TODO, f"Add: {field['options']} is not written yet")
            except SqlProblem as e:
                return report(FAIL, f"Add: {field['options']} has an error", e.message)
            except KeyError:
                return report(FAIL, f"Add: the {field['name']} dropdown has no \"options\" file in settings.py")
            if not rows:
                return report(FAIL, f"Add: {field['options']} returns no choices")
            sample[field["name"]] = rows[0][0]
        elif kind == "number":
            sample[field["name"]] = 1
        elif kind == "date":
            sample[field["name"]] = "2026-01-15"
        else:
            sample[field["name"]] = "Test"
    # Tried inside a SAVEPOINT and then undone, so nothing is kept.
    conn.execute("SAVEPOINT trial")
    try:
        run(conn, project, "queries/add.sql", sample)
        report(PASS, "Add: queries/add.sql saves a test row")
    except NotWritten:
        report(TODO, "Add: queries/add.sql is not written yet")
    except SqlProblem as e:
        report(FAIL, "Add: queries/add.sql has an error", e.message)
    finally:
        conn.execute("ROLLBACK TO trial")


def finish():
    done = results.count(PASS)
    print(f"\n{done} done, {results.count(TODO)} still to do, {results.count(FAIL)} to fix.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
