/* add_author_options.sql   ADD PAGE: the choices in the Author dropdown
   Returns two columns: first the id that gets saved, then the text the
   visitor sees. settings.py names this file in the "options" of the
   author_id box.
   Placeholders: none. */

SELECT author_id, name
FROM authors
ORDER BY name;
