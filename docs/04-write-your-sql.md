# Part 4. Write your SQL

This is the main part of the project. You plan a database for a topic you choose, then write one SQL file at a time. After each step you save, refresh the browser, and see another page come to life.

**Keep the app running the whole time** (Part 3, Start the app). Saving a SQL file rebuilds the database automatically. Keep a second terminal open for `python check.py`.

**Comment every statement.** Above each statement, write a short comment in your own words saying what it does. Start a comment with two dashes:

```sql
-- every recipe with its cuisine, newest first
SELECT ...
```

The comments are graded.

## Step 0. Plan your topic

1. **Pick something you know and care about.** Some ideas:

   | Topic | Main thing (one row on Browse) | A parent it belongs to | Things that happen to it |
   |---|---|---|---|
   | Recipe box | recipes | cuisines | reviews |
   | Video game library | games | studios | play sessions |
   | Pet shelter | pets | species | adoptions |
   | Movie watchlist | movies | directors | ratings |
   | Sports league | players | teams | games played |
   | Car service log | cars | owners | services |
   | Plant care | plants | rooms | waterings |
   | Club roster | members | clubs | events attended |

   The library follows the same pattern: books (main thing), authors (parent), loans (things that happen, linking books to members).

2. **List your tables and their columns** on paper. For each table, write its primary key first, then the columns, then which columns are foreign keys.
3. **Check third normal form.** Every column must describe the key, the whole key, and nothing but the key. If a value would be typed again and again (an author's country in every book row, for example), it belongs in its own table. The class page on normalization at cruzjohal.com/database/normalization has many examples.
4. **Draw the ER diagram.** Use [draw.io](https://app.diagrams.net/) (free) or draw it neatly on paper and take a photo. Save it in the top folder of your project as **erd.png**.

   **Have Generative AI check your diagram.** Open a generative AI tool such as ChatGPT, Claude, Gemini, or Microsoft Copilot. Upload `erd.png` and paste this prompt:

   ```text
   I am a database student. This is the ER diagram for my SQLite project about <your topic>.
   Please check it and list any corrections. For each table, check:
   1. Does it have a primary key?
   2. Are the foreign keys correct, and do they point at the right parent table?
   3. Are the relationships (one to many, many to many) drawn correctly?
   4. Is it in third normal form? Point out any repeated or misplaced columns.
   5. Are any tables or columns missing, unneeded, or poorly named?
   Explain each correction in plain language. Do not redraw the diagram for me.
   ```

   Then:

   1. **Read every suggestion and decide for yourself.** AI tools make mistakes. Keep the corrections that are right for your topic and skip the ones that are not.
   2. **Fix your diagram** and save it again as `erd.png`. Update your table list from step 2 to match.
   3. **Save the AI's corrections as a PDF** named **erd-ai-review.pdf** in the top folder of your project, next to `erd.png`. Include:
      * the name of the AI tool you used and the date,
      * the prompt you sent,
      * the AI's full response (copy and paste it, or print the chat page to PDF), and
      * a short note in your own words saying which corrections you made and which you skipped, and why.

   To make the PDF, paste everything into a Word or Google Docs document and choose **File > Save as PDF** (Word) or **File > Download > PDF Document** (Google Docs).
5. **Make up your data.** Use made up names. For emails, use addresses ending in `@example.com`, which is reserved for examples. Never use real people's personal information.

## Step 1. Switch to your project

1. Open `config.py`.
2. Change the line to:

   ```python
   PROJECT_FOLDER = "my_project"
   ```

3. Save. The app restarts by itself.
4. Refresh the browser. Every page now shows a yellow box saying **This page is waiting for its SQL** and names the file to write. That is your to do list.

## Step 2. Name your site

Open `projects/my_project/settings.py` and fill in each line. Change only the text inside the quotes.

* `SITE_NAME`, `TAGLINE`, `YOUR_NAME`, `COURSE`
* `ICON`: pick any icon at [icons.getbootstrap.com](https://icons.getbootstrap.com/) and use its name without `bi-`, such as `egg-fried`, `controller`, or `music-note-beamed`.
* `ITEM` and `ITEMS`: what one row on Browse is called, like `"recipe"` and `"recipes"`.
* The titles and intros for each page.

Leave `ADD_FORM` empty for now. Save and refresh: the name at the top changes.

## Step 3. Create your tables (schema.sql)

Open `projects/my_project/schema.sql`. Write one `CREATE TABLE` for each table, **parent tables first**, because a foreign key can only point at a table that already exists.

The pattern, from the library:

```sql
-- each author once
CREATE TABLE authors (
    author_id  INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    country    TEXT
);

-- each book once, pointing at its author
CREATE TABLE books (
    book_id         INTEGER PRIMARY KEY,
    title           TEXT NOT NULL,
    author_id       INTEGER NOT NULL,
    year_published  INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
```

**SQLite is a little different from MySQL:**

| You want | MySQL | SQLite |
|---|---|---|
| A numbered primary key | `INT AUTO_INCREMENT PRIMARY KEY` | `INTEGER PRIMARY KEY` |
| Text | `VARCHAR(40)` | `TEXT` (VARCHAR works too) |
| Whole number / decimal | `INT` / `DECIMAL(5,2)` | `INTEGER` / `REAL` |
| A date | `DATE` | `TEXT` holding `'2026-03-15'` |
| Join text together | `CONCAT(a, ' ', b)` | `a \|\| ' ' \|\| b` |
| Stored procedures | yes | no (SQLite has none) |

Save, then run `python check.py`. The Tables section should list your tables. If a step shows FAIL, it names the file, the line, and what went wrong.

## Step 4. Add your sample rows (seed.sql)

Open `projects/my_project/seed.sql`. Write `INSERT` statements, **parent rows first**. Give every table **at least 10 rows**. One INSERT can add many rows:

```sql
-- the authors. ids given so the books can point at them
INSERT INTO authors (author_id, name, country) VALUES
    (1, 'Jane Austen',  'England'),
    (2, 'Mary Shelley', 'England'),
    (3, 'Mark Twain',   'United States');
```

* Text and dates go in single quotes. Numbers and `NULL` do not.
* A name with an apostrophe doubles it: `'O''Brien'`.
* A comma goes between rows. A semicolon goes only after the last row.

Save, then run `python check.py`. Each table should show its row count.

## Step 5. Home page numbers (queries/stats.sql)

One row, one column per number. The alias in double quotes becomes the label.

```sql
-- the counts for the home page
SELECT
    (SELECT COUNT(*) FROM books)   AS "Books",
    (SELECT COUNT(*) FROM authors) AS "Authors";
```

Use 2 to 4 numbers. At least one should be more interesting than a plain count, such as a count with a WHERE (`loans WHERE returned_on IS NULL`) or an average. Save and refresh the Home page.

## Step 6. Browse page (queries/list.sql)

Every row of your main table, joined to its parent so it shows names instead of id numbers.

```sql
-- every book with its author's name, newest first
SELECT b.book_id         AS id,
       b.title           AS "Title",
       a.name            AS "Author",
       b.year_published  AS "Year"
FROM books b
JOIN authors a ON a.author_id = b.author_id
ORDER BY b.year_published DESC;
```

* **You must include a column named `id`.** The page hides it and uses it to link each row to its detail page.
* The first column after `id` becomes the link, so put the name or title there.
* The aliases become the column headings. Double quotes allow spaces.

Save and refresh Browse.

## Step 7. Detail page (queries/detail.sql)

One row: everything about the item that was clicked. `:id` is a **placeholder**. When someone clicks a row, the app fills it in with that row's id.

```sql
-- one book with its author's details
SELECT b.book_id   AS id,
       b.title     AS "Title",
       a.name      AS "Author",
       a.country   AS "Author's country",
       b.pages     AS "Pages"
FROM books b
JOIN authors a ON a.author_id = b.author_id
WHERE b.book_id = :id;
```

The first column after `id` becomes the page heading. Try adding a subquery, like the library's "Times borrowed" count. Test it on its own with:

```
python try_sql.py projects/my_project/queries/detail.sql id=1
```

## Step 8. Related rows (queries/detail_related.sql)

The table under the item on its detail page: the rows from your third table that belong to it. It gets the same `:id`.

```sql
-- every time this book was borrowed, and by whom
SELECT m.name                                AS "Member",
       l.loaned_on                           AS "Borrowed",
       COALESCE(l.returned_on, 'Still out')  AS "Returned"
FROM loans l
JOIN members m ON m.member_id = l.member_id
WHERE l.book_id = :id
ORDER BY l.loaned_on DESC;
```

Set `DETAIL_RELATED_TITLE` in settings.py to match, like "Reviews" or "Play sessions".

## Step 9. Search page (queries/search.sql)

The same columns as Browse (including `id`), filtered by what the visitor typed. `:term` holds the search words.

```sql
-- books whose title or author contains the search words
SELECT b.book_id  AS id,
       b.title    AS "Title",
       a.name     AS "Author"
FROM books b
JOIN authors a ON a.author_id = b.author_id
WHERE b.title LIKE '%' || :term || '%'
   OR a.name  LIKE '%' || :term || '%'
ORDER BY b.title;
```

`'%' || :term || '%'` puts a % on each side of the words, so they can appear anywhere. Search at least two columns.

> **Why a placeholder?** The search words go in through `:term`, separately from the SQL. If the app pasted them into the SQL text instead, a visitor could type SQL of their own and run it. That attack is called **SQL injection**, and placeholders are how real applications prevent it.

## Step 10. Report page (queries/report.sql)

A summary with `GROUP BY`: one row per group, with a count, average, or total for each.

```sql
-- how many books in each genre, and their average length
SELECT genre              AS "Genre",
       ROUND(AVG(pages))  AS "Average pages",
       COUNT(*)           AS "Books"
FROM books
GROUP BY genre
ORDER BY COUNT(*) DESC;
```

If the **last** column is a number, the page draws a bar for it, so put the number you most want to compare last. Set `REPORT_TITLE` and `REPORT_INTRO` in settings.py to describe it.

## Step 11. Add page (settings.py, add_options.sql, add.sql)

The Add page is a form that inserts a row into your main table. It takes three pieces.

1. **List the boxes** in `ADD_FORM` in settings.py, one per column you want typed in. Leave out the primary key; SQLite numbers new rows itself.

   ```python
   ADD_FORM = [
       {"name": "title", "label": "Title", "type": "text", "required": True},
       {"name": "author_id", "label": "Author", "type": "select",
        "options": "queries/add_options.sql", "required": True},
       {"name": "pages", "label": "Pages", "type": "number"},
   ]
   ```

   The types are `text`, `number`, `date`, and `select` (a dropdown).

2. **Fill the dropdown** in `queries/add_options.sql`. A foreign key column should be a dropdown, so visitors pick a name instead of typing an id. Return two columns: the id to save, then the text to show.

   ```sql
   -- the authors to choose from, by name
   SELECT author_id, name
   FROM authors
   ORDER BY name;
   ```

3. **Write the INSERT** in `queries/add.sql`. Each placeholder matches a `name` from ADD_FORM.

   ```sql
   -- save the form as a new book
   INSERT INTO books (title, author_id, pages)
   VALUES (:title, :author_id, :pages);
   ```

Save, refresh the Add page, and add a row. It appears on Browse. Remember that rows added on the website are temporary.

## Step 12. CIS 4720: a view and a trigger

Add these at the **bottom** of schema.sql, after the tables they use.

**A view** is a saved SELECT that you can query like a table:

```sql
-- each book joined to its author once, so other queries stay short
CREATE VIEW book_catalog AS
SELECT b.book_id, b.title, a.name AS author, b.genre
FROM books b
JOIN authors a ON a.author_id = b.author_id;
```

Then use it somewhere, for example change list.sql to `SELECT ... FROM book_catalog`.

**A trigger** runs by itself when a row is inserted, updated, or deleted. SQLite triggers look a little different from MySQL's. The most useful kind for this project checks new rows and refuses bad ones with `RAISE`:

```sql
-- refuse a book whose year is in the future
CREATE TRIGGER check_book_year
BEFORE INSERT ON books
FOR EACH ROW
WHEN NEW.year_published > CAST(strftime('%Y', 'now') AS INTEGER)
BEGIN
    SELECT RAISE(ABORT, 'Year published cannot be in the future');
END;
```

Test it on your Add page by entering a value the trigger should refuse. Its message appears on the page.

## Step 13. Finish up

1. Run `python check.py`. Every line should say PASS.
2. Click through every page one more time, including a search that finds nothing and a detail page.
3. Put `erd.png` and `erd-ai-review.pdf` in the top folder of your project.
4. Open `README.md` and fill in the top section: your site's name, a description, your tables, and (after Part 6) your live Render address.
5. Check that every statement in every SQL file has a comment above it.

Next: [Part 5. Save to GitHub](05-save-to-github.md). Do this often, not just at the end.
