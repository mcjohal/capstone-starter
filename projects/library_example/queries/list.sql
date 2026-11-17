/* list.sql   BROWSE PAGE: every item in a table
   Returns many rows. Must include a column named id: the page hides it
   and uses it to link each row to its detail page. Every other column
   is shown, with its alias as the column heading.
   Placeholders: none.
   This one reads from the book_catalog view (see schema.sql), which has
   already joined each book to its author. */

SELECT book_id         AS id,
       title           AS "Title",
       author          AS "Author",
       genre           AS "Genre",
       year_published  AS "Year"
FROM book_catalog
ORDER BY year_published DESC;
