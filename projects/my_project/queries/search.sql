/* search.sql   SEARCH PAGE: rows that match what the visitor typed      (Part 4, Step 9 of the guide)
   Returns many rows, with a column named id, just like list.sql.
   Placeholders:  :term   the words typed in the search box
   '%' || :term || '%' glues a % on each side of the search words, so
   LIKE finds them anywhere in the text. || is how SQLite joins text
   (MySQL uses CONCAT). In SQLite, LIKE ignores upper and lower case.
   The words go in through the :term placeholder, never pasted into the
   SQL itself. That is what keeps the search safe from SQL injection.

   The library version: projects/library_example/queries/search.sql
   Write your SQL below this comment. */

