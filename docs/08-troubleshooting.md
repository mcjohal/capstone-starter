# Troubleshooting

Find the message you see, then follow the fix. Most problems are a missing comma, quote, or semicolon.

## Running the app in VS Code

**`python` is not recognized** (Windows)
Python is not on your PATH. Run the Python installer again, choose **Modify**, turn on **Add Python to environment variables**, then close and reopen VS Code. On a Mac, use `python3`.

**`No module named flask`**
VS Code is not using the project's environment. Press Ctrl + Shift + P, run **Python: Select Interpreter**, and choose the one with `.venv`. Then open a new terminal. If there is no `.venv` folder, do Set up a Python environment in Part 3.

**`running scripts is disabled on this system`** (Windows terminal)
PowerShell is blocking the environment's start script. Click the down arrow next to the **+** on the terminal panel, choose **Command Prompt**, and use that terminal instead.

**`Address already in use` or port 5000 is busy**
The app is already running in another terminal. Find that terminal and press Ctrl + C, or close it with the trash can icon. On a Mac, port 5000 can be taken by AirPlay Receiver: turn it off in System Settings, General, AirDrop and Handoff.

**I changed a file but the page did not change**
Save the file (a dot on the file's tab means unsaved), wait two seconds, and refresh. If you changed `config.py` or `settings.py` and nothing happens, stop the app with Ctrl + C and start it again.

## SQL errors

The page, `check.py`, and `try_sql.py` all name the file and the line where the statement starts. Look on that line and the few after it.

| Message contains | What it usually means | Fix |
|---|---|---|
| `syntax error` near a word | Something is missing just before that word | Look for a missing comma between columns or values, a missing quote, or a missing parenthesis |
| `never ends` | The statement has no semicolon, or a quote was opened and never closed | Add the `;`, or find the text missing its closing `'` |
| `has no column named` | An INSERT names a column the table doesn't have | Check the spelling. If it is spelled right, look for a **missing comma** at the end of the line above it in CREATE TABLE |
| `no such column` | A query names a column that doesn't exist | Check the spelling and the table alias (`b.title`, not `a.title`) |
| `no such table` | The table name is wrong, or the table is created later in the file | Check the spelling, and put parent tables first |
| `FOREIGN KEY constraint failed` | A row points at a parent row that doesn't exist | Insert parent rows first, and check the id numbers |
| `UNIQUE constraint failed` | Two rows have the same value in a unique column or primary key | Give each row its own id |
| `values for N columns` | The INSERT lists a different number of columns and values | Count them. Usually a missing value or comma |
| `only execute one statement` | A query file holds two statements | Each file in `queries` holds exactly one |
| `did not supply a value for binding parameter` | The query uses a placeholder this page doesn't provide | Detail pages provide `:id`, Search provides `:term`, and Add provides one per ADD_FORM box |

**A page says it needs a column named id**
`list.sql` and `search.sql` must include the primary key renamed to id: `SELECT recipe_id AS id, ...`

**My apostrophe breaks everything**
Inside single quotes, write an apostrophe twice: `'O''Brien'`, `'Grandma''s Pie'`.

## GitHub and Render

See If something goes wrong in [Part 5](05-save-to-github.md#if-something-goes-wrong) and If the deploy fails in [Part 6](06-deploy-to-render.md#if-the-deploy-fails).

**My live site takes a minute to load**
Normal on the free tier. It sleeps after about 15 minutes without visitors and takes up to a minute to wake.

**Rows I added on my live site disappeared**
Normal. The database is rebuilt from your SQL files every time the app starts. Put anything you want to keep in `seed.sql`, then commit and push.
