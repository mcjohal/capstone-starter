/* detail.sql   DETAIL PAGE: one item, everything about it
   Returns ONE row (or none, if the id does not exist). The first column
   after id becomes the page heading; every other column is listed below
   it with its alias as the label.
   Placeholders:  :id   the id of the row that was clicked
   The JOIN brings in the author's details from the authors table, and
   the subquery counts how many times this book was borrowed. */

SELECT b.book_id           AS id,
       b.title             AS "Title",
       a.name              AS "Author",
       a.country           AS "Author's country",
       b.genre             AS "Genre",
       b.year_published    AS "Year published",
       b.pages             AS "Pages",
       (SELECT COUNT(*) FROM loans l WHERE l.book_id = b.book_id) AS "Times borrowed"
FROM books b
JOIN authors a ON a.author_id = b.author_id
WHERE b.book_id = :id;
