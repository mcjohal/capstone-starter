"""Runs SQL against a fresh copy of your database and prints the result.

Use it to test a query before (or instead of) refreshing the website.
Run these in the VS Code terminal:

    python try_sql.py projects/my_project/queries/list.sql
    python try_sql.py projects/my_project/queries/detail.sql id=3
    python try_sql.py projects/my_project/queries/search.sql term=war
    python try_sql.py "SELECT * FROM books LIMIT 5"
    python try_sql.py scratch.sql

Placeholders like :id and :term get their values from name=value pairs
after the file name. The database is built in memory from your schema.sql
and seed.sql, so nothing you run here changes anything.
"""

import sqlite3
import sys
from pathlib import Path

import config
from database import NotWritten, Project, SqlProblem, friendly, split_statements


def print_table(columns, rows, limit=50):
    if not columns:
        print("(done, no rows to show)")
        return
    shown = [["" if v is None else str(v) for v in row] for row in rows[:limit]]
    widths = [min(max([len(c)] + [len(r[i]) for r in shown]), 40) for i, c in enumerate(columns)]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("| " + " | ".join(c[:w].ljust(w) for c, w in zip(columns, widths)) + " |")
    print(line)
    for row in shown:
        print("| " + " | ".join(v[:w].ljust(w) for v, w in zip(row, widths)) + " |")
    print(line)
    extra = f", showing the first {limit}" if len(rows) > limit else ""
    print(f"{len(rows)} row{'s' if len(rows) != 1 else ''}{extra}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    target, pairs = sys.argv[1], sys.argv[2:]
    params = {}
    for pair in pairs:
        if "=" not in pair:
            print(f"Write placeholder values as name=value, for example id=3 (got {pair})")
            return 1
        key, value = pair.split("=", 1)
        params[key.lstrip(":")] = int(value) if value.lstrip("-").isdigit() else value

    path = Path(target)
    sql = path.read_text(encoding="utf-8") if path.suffix.lower() == ".sql" and path.exists() else target
    if path.suffix.lower() == ".sql" and not path.exists():
        print(f"There is no file at {target}. Check the path and spelling.")
        return 1

    project = Project(config.PROJECT_FOLDER)
    conn = sqlite3.connect(":memory:")
    try:
        project.load_into(conn)
    except NotWritten as e:
        print(f"Note: {e.path} is empty, so the database has no tables or rows from it yet.\n")
    except SqlProblem as e:
        print(f"Your database could not be built. {e}\n")
        return 1

    statements = list(split_statements(sql))
    if not statements:
        print("That has no SQL in it yet.")
        return 1
    for line, statement in statements:
        if len(statements) > 1:
            print(f"\nStatement starting on line {line}:")
        try:
            cursor = conn.execute(statement, params)
        except (sqlite3.Error, sqlite3.Warning) as e:
            print(f"SQLite found a problem: {friendly(e)}")
            return 1
        columns = [d[0] for d in cursor.description] if cursor.description else []
        print_table(columns, cursor.fetchall())
    return 0


if __name__ == "__main__":
    sys.exit(main())
