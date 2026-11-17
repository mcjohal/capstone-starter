/* ==========================================================================
   schema.sql   Valley Library (the example)
   The tables. The app runs this file first, every time it starts.

   Four tables in third normal form:
     authors   one row per author
     books     one row per book, pointing at its author
     members   one row per library card holder
     loans     one row each time a member borrows a book
               (this is how books and members connect: many to many)
   ========================================================================== */

-- Each author once. INTEGER PRIMARY KEY makes SQLite number the rows
-- for us, the way AUTO_INCREMENT does in MySQL.
CREATE TABLE authors (
    author_id  INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    country    TEXT,
    born_year  INTEGER
);

-- Each book once. author_id is a foreign key: it must match an author.
-- The author's name is NOT stored here, only the id, so it is never
-- typed twice (that would be a transitive dependency).
CREATE TABLE books (
    book_id         INTEGER PRIMARY KEY,
    title           TEXT NOT NULL,
    author_id       INTEGER NOT NULL,
    genre           TEXT,
    year_published  INTEGER,
    pages           INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Each library member once. UNIQUE stops two members sharing an email.
CREATE TABLE members (
    member_id  INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE,
    joined_on  TEXT          -- SQLite stores dates as text, YYYY-MM-DD
);

-- One row per borrowing. Two foreign keys link a book to a member.
-- returned_on stays NULL while the book is still checked out.
CREATE TABLE loans (
    loan_id      INTEGER PRIMARY KEY,
    book_id      INTEGER NOT NULL,
    member_id    INTEGER NOT NULL,
    loaned_on    TEXT NOT NULL,
    returned_on  TEXT,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);


/* --------------------------------------------------------------------------
   CIS 4720: a view and a trigger
   -------------------------------------------------------------------------- */

-- A view is a saved SELECT you can query like a table. This one joins
-- each book to its author once, so list.sql and search.sql stay short.
CREATE VIEW book_catalog AS
SELECT b.book_id,
       b.title,
       a.name AS author,
       b.genre,
       b.year_published,
       b.pages
FROM books b
JOIN authors a ON a.author_id = b.author_id;

-- A trigger runs by itself when something happens to a table. This one
-- checks every new book and refuses a year in the future. Try it on the
-- Add page with the year 2999. RAISE(ABORT, ...) cancels the INSERT and
-- shows the message.
CREATE TRIGGER check_book_year
BEFORE INSERT ON books
FOR EACH ROW
WHEN NEW.year_published > CAST(strftime('%Y', 'now') AS INTEGER)
BEGIN
    SELECT RAISE(ABORT, 'Year published cannot be in the future');
END;
