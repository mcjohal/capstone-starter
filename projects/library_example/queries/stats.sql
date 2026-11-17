/* stats.sql   HOME PAGE: the numbers across the top
   Returns ONE row. Each column becomes one number on the page, and the
   column's alias (the name after AS, in double quotes) is its label.
   Placeholders: none.
   Each number comes from its own small SELECT inside parentheses,
   called a subquery. */

SELECT
    (SELECT COUNT(*) FROM books)                              AS "Books",
    (SELECT COUNT(*) FROM authors)                            AS "Authors",
    (SELECT COUNT(*) FROM members)                            AS "Members",
    (SELECT COUNT(*) FROM loans WHERE returned_on IS NULL)    AS "Checked out now";
