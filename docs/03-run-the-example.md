# Part 3. Run the example

Before writing anything, run the finished library app and see how each page connects to a SQL file. Allow about 30 minutes.

## Set up a Python environment (once)

A virtual environment is a private copy of Python for this project, with Flask installed in it.

1. In VS Code, press **Ctrl + Shift + P** to open the Command Palette (Cmd + Shift + P on a Mac).
2. Type **Python: Create Environment** and press Enter.
3. Choose **Venv**.
4. Choose the Python version you installed (the newest one in the list).
5. When it asks about dependencies, check **requirements.txt** and click **OK**.
6. Wait for the message at the bottom right to finish. A `.venv` folder appears in the Explorer.

From now on, every new terminal in this folder starts with `(.venv)` at the beginning of the prompt. That means the environment is on.

## Start the app

1. Open `app.py` in the Explorer.
2. Click the **Run Python File** button (a triangle) at the top right of the editor.
3. The terminal prints a few lines, including `Running on http://127.0.0.1:5000`.
4. Hold **Ctrl** and click that address, or type it into your browser.

You should see **Valley Library**, with a yellow strip at the top saying you are looking at the example.

To **stop** the app later: click in the terminal and press **Ctrl + C**.

> If you see `No module named flask`, VS Code is using the wrong Python. Press Ctrl + Shift + P, run **Python: Select Interpreter**, choose the one that says `.venv`, then run `app.py` again.

## Match each page to its SQL

Keep the browser and VS Code side by side. For each page, open its SQL file in `projects/library_example/` and read it.

1. **Home.** The four numbers come from `queries/stats.sql`. Each `AS "Books"` alias becomes a label.
2. **Browse.** The table comes from `queries/list.sql`. Notice `book_id AS id`: the page hides the id column and uses it to link each title.
3. Click a title. **Detail** runs `queries/detail.sql` with `:id` set to that book's id. The table under it, Loan history, is `queries/detail_related.sql`.
4. **Search.** Search for `wells`. That runs `queries/search.sql` with `:term` set to what you typed.
5. **Report.** `queries/report.sql` uses GROUP BY. The bars come from its last column.
6. **Add.** The boxes on the form are listed in `settings.py` under `ADD_FORM`, and saving runs `queries/add.sql`. Add a book, then find it on Browse. Now try the year 2999: the trigger in `schema.sql` refuses it.

## Watch the app rebuild itself

1. Open `projects/library_example/seed.sql`.
2. Change the title `'Moby Dick'` to `'Moby Dick or The Whale'` and save (Ctrl + S).
3. Wait two seconds and refresh Browse. The new title is there, because the app rebuilt the database from the SQL files.
4. Notice the book you added on the Add page is gone. **Rows added on the website are temporary.** Anything you want to keep goes in `seed.sql`.
5. Change the title back and save.

## Try the two tools

1. Open a second terminal with the **+** button on the terminal panel, so the app keeps running in the first one.
2. Run the checker on the example. Everything should say PASS:

   ```
   python check.py library_example
   ```

3. Run a query file by itself. The result prints as a table:

   ```
   python try_sql.py projects/library_example/queries/detail.sql id=3
   ```

4. Open `scratch.sql`, change the SELECT to `SELECT * FROM books LIMIT 5;`, save, and run:

   ```
   python try_sql.py scratch.sql
   ```

   `try_sql.py` always uses the project named in `config.py`, so these tables are the library's for now.

Next: [Part 4. Write your SQL](04-write-your-sql.md)
