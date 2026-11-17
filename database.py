"""Everything that talks to the database lives here.

You should not need to change this file. Your work goes in the SQL files
inside projects/my_project/ (see docs/04-write-your-sql.md).

How the database works in this app
----------------------------------
Every time the app starts, it builds a brand new SQLite database by running
your schema.sql (the tables) and then your seed.sql (the sample rows).
Each page then runs one of your query files from the queries folder.

That means:
  * Your SQL files are the real database. Change them, save, and the app
    rebuilds itself from them.
  * Rows added on the website's Add page are temporary. They disappear the
    next time the app restarts, which on Render's free tier happens often.
    Anything you want to keep belongs in seed.sql.
"""

import os
import re
import runpy
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "app.db"


class NotWritten(Exception):
    """A SQL file that is still empty (only comments)."""

    def __init__(self, path):
        super().__init__(f"{path} has no SQL in it yet.")
        self.path = path


class SqlProblem(Exception):
    """SQLite refused a statement. Carries the file and line so the page
    can say exactly where to look."""

    def __init__(self, path, message, line=None):
        where = f"{path}, statement starting on line {line}" if line else str(path)
        super().__init__(f"{where}: {message}")
        self.path = path
        self.message = message
        self.line = line


class Result:
    def __init__(self, columns, rows):
        self.columns = columns          # column names, from your AS aliases
        self.rows = rows                # list of tuples

    def as_dicts(self):
        return [dict(zip(self.columns, row)) for row in self.rows]

    def first(self):
        return dict(zip(self.columns, self.rows[0])) if self.rows else None


def strip_comments(sql):
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S)
    return "\n".join(line.split("--", 1)[0] for line in sql.splitlines())


def has_sql(sql):
    return bool(strip_comments(sql).strip())


def split_statements(sql):
    """Yields (line_number, statement) for each complete statement, using
    SQLite's own rules (so a CREATE TRIGGER with semicolons inside its
    BEGIN ... END block counts as one statement)."""
    # Blank out /* ... */ comments but keep their line breaks, so the line
    # numbers still match the file and a comment is never mistaken for
    # the start of a statement.
    blanked = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group()), sql, flags=re.S)
    code_lines = [line.split("--", 1)[0] for line in blanked.splitlines()]
    buffer, start = "", None
    for number, line in enumerate(sql.splitlines(), start=1):
        if start is None and number <= len(code_lines) and code_lines[number - 1].strip():
            start = number
        buffer += line + "\n"
        if start is not None and sqlite3.complete_statement(buffer):
            yield start, buffer
            buffer, start = "", None
    if start is not None:
        yield start, buffer   # unfinished, probably a missing semicolon


def friendly(error):
    """Adds a hint to the SQLite errors beginners hit most."""
    text = str(error)
    hints = {
        "no such table": "Check the table name, and that schema.sql creates it.",
        "no such column": "Check the column name and its table alias (b.title, a.name, and so on).",
        "has no column named": "Check that schema.sql creates that column. If it does, look for a "
                               "missing comma at the end of the line above it in CREATE TABLE.",
        "values for": "The number of values must match the number of columns listed. "
                      "Look for a missing value or a missing comma.",
        "syntax error": "Look just before the word in quotes: a missing comma, quote, or parenthesis is the usual cause.",
        "FOREIGN KEY constraint failed": "A foreign key points at a row that does not exist. "
                                         "Insert the parent row first, or fix the id.",
        "UNIQUE constraint failed": "Two rows have the same value in a column that must be unique.",
        "NOT NULL constraint failed": "A required column was left empty.",
        "incomplete input": "The statement is unfinished. Look for a missing semicolon or closing parenthesis.",
        "You can only execute one statement at a time": "A query file may hold only one SELECT (or one INSERT). "
                                                        "Remove the extra statement.",
        "Binding": "Use named placeholders like :id or :term, not a question mark.",
        "did not supply a value for binding parameter": "This page only supplies the placeholders "
                                                        "listed at the top of the file.",
    }
    for key, hint in hints.items():
        if key in text:
            return f"{text}. {hint}"
    return text


class Project:
    """One project folder: projects/<name>/ with settings.py, schema.sql,
    seed.sql, and a queries folder."""

    def __init__(self, name):
        self.name = name
        self.folder = PROJECTS_DIR / name
        if not self.folder.is_dir():
            raise SystemExit(f"config.py says PROJECT_FOLDER = '{name}', but there is no "
                             f"folder named projects/{name}. Check the spelling.")
        self.settings = runpy.run_path(str(self.folder / "settings.py"))
        self.settings = {k: v for k, v in self.settings.items() if k.isupper()}
        self.build_problem = None

    # -- files ---------------------------------------------------------------

    def path(self, relative):
        return self.folder / relative

    def display_path(self, relative):
        return f"projects/{self.name}/{relative}"

    def read(self, relative):
        """The SQL in a file, or NotWritten if it holds only comments."""
        file = self.path(relative)
        sql = file.read_text(encoding="utf-8") if file.exists() else ""
        if not has_sql(sql):
            raise NotWritten(self.display_path(relative))
        return sql

    def sql_files(self):
        return sorted(str(p) for p in self.folder.rglob("*.sql"))

    # -- building the database -------------------------------------------------

    def load_into(self, conn):
        """Runs schema.sql then seed.sql into an open connection, one
        statement at a time so an error can name its line."""
        conn.execute("PRAGMA foreign_keys = ON")
        for relative in ("schema.sql", "seed.sql"):
            sql = self.read(relative)
            for line, statement in split_statements(sql):
                if not sqlite3.complete_statement(statement):
                    raise SqlProblem(self.display_path(relative),
                                     "this statement never ends. Look for a missing semicolon at its end, "
                                     "or a quote mark (') that was opened and never closed.", line)
                try:
                    conn.execute(statement)
                except sqlite3.Error as e:
                    raise SqlProblem(self.display_path(relative), friendly(e), line)
        conn.commit()

    def build_database(self):
        """Builds a fresh database file from the SQL files. It is built under
        a temporary name and then swapped in, so a half built database is
        never used."""
        INSTANCE_DIR.mkdir(exist_ok=True)
        temp = INSTANCE_DIR / f"building-{os.getpid()}.db"
        temp.unlink(missing_ok=True)
        conn = sqlite3.connect(temp)
        try:
            self.load_into(conn)
            self.build_problem = None
        except (NotWritten, SqlProblem) as e:
            self.build_problem = e
        finally:
            conn.close()
        os.replace(temp, DB_PATH)

    # -- running queries ---------------------------------------------------------

    def connect(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def query(self, relative, params=None):
        """Runs one SELECT file and returns a Result."""
        sql = self.read(relative)
        conn = self.connect()
        try:
            cursor = conn.execute(sql, params or {})
            columns = [d[0] for d in cursor.description] if cursor.description else []
            return Result(columns, cursor.fetchall())
        except (sqlite3.Error, sqlite3.Warning) as e:
            raise SqlProblem(self.display_path(relative), friendly(e))
        finally:
            conn.close()

    def change(self, relative, params):
        """Runs one INSERT (or UPDATE or DELETE) file and saves it. Returns
        the id of the new row."""
        sql = self.read(relative)
        conn = self.connect()
        try:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        except (sqlite3.Error, sqlite3.Warning) as e:
            raise SqlProblem(self.display_path(relative), friendly(e))
        finally:
            conn.close()
