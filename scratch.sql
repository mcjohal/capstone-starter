/* scratch.sql   A place to try out SQL. The app never reads this file.

   Write any SELECT here, save, then run it in the terminal:

       python try_sql.py scratch.sql

   It runs against a fresh copy of your database, built from your
   schema.sql and seed.sql, so you can't break anything. */

SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
