/* search.sql   SEARCH PAGE: rows that match what the visitor typed
   Returns many rows, with a column named id, just like list.sql.
   Placeholders:  :term   the words typed in the search box
   '%' || :term || '%' glues a % on each side of the search words, so
   LIKE finds them anywhere in the text. || is how SQLite joins text
   (MySQL uses CONCAT). In SQLite, LIKE ignores upper and lower case.
   The words go in through the :term placeholder, never pasted into the
   SQL itself. That is what keeps the search safe from SQL injection. */

SELECT book_id   AS id,
       title     AS "Title",
       author    AS "Author",
       genre     AS "Genre"
FROM book_catalog
WHERE title  LIKE '%' || :term || '%'
   OR author LIKE '%' || :term || '%'
   OR genre  LIKE '%' || :term || '%'
ORDER BY title;
