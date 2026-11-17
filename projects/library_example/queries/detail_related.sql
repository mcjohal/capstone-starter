/* detail_related.sql   DETAIL PAGE: the table under the item
   Returns many rows that belong to the item on the detail page, shown as
   a table. Its heading is DETAIL_RELATED_TITLE in settings.py.
   Placeholders:  :id   the same id as detail.sql
   Each loan of this book, joined to the member who borrowed it.
   COALESCE shows the words "Still out" when returned_on is NULL. */

SELECT m.name                              AS "Member",
       l.loaned_on                         AS "Borrowed",
       COALESCE(l.returned_on, 'Still out') AS "Returned"
FROM loans l
JOIN members m ON m.member_id = l.member_id
WHERE l.book_id = :id
ORDER BY l.loaned_on DESC;
