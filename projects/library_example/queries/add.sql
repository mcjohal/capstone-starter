/* add.sql   ADD PAGE: saves the form as a new row
   One INSERT. Each placeholder matches the "name" of a box in ADD_FORM
   in settings.py: the Title box fills :title, the Author dropdown fills
   :author_id, and so on. An empty box arrives as NULL.
   book_id is left out, so SQLite numbers the new row itself.
   The check_book_year trigger in schema.sql runs before this INSERT. */

INSERT INTO books (title, author_id, genre, year_published, pages)
VALUES (:title, :author_id, :genre, :year_published, :pages);
