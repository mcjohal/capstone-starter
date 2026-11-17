/* report.sql   REPORT PAGE: a summary with GROUP BY
   Returns one row per group. If the LAST column is a number, the page
   also draws a bar for it, so put the number you want to compare last.
   Placeholders: none.
   GROUP BY makes one row per genre. COUNT, AVG, and ROUND work on each
   group separately. */

SELECT genre               AS "Genre",
       ROUND(AVG(pages))   AS "Average pages",
       COUNT(*)            AS "Books"
FROM books
GROUP BY genre
ORDER BY COUNT(*) DESC, genre;
