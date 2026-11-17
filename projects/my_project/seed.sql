/* ==========================================================================
   seed.sql   YOUR SAMPLE ROWS                     (Part 4, Step 4 of the guide)
   The app runs this right after schema.sql, every time it starts. This is
   the data your site shows, so make it realistic.

   Requirements
     * At least 10 rows in every table.
     * Parent rows first: a row must exist before a foreign key points at it.
     * Text and dates go in single quotes: 'Ana Lopez', '2026-03-15'.
       Numbers and NULL do not.
     * A name with an apostrophe doubles it: 'O''Brien'.

   One INSERT can add many rows, separated by commas:
       INSERT INTO authors (author_id, name) VALUES
           (1, 'Jane Austen'),
           (2, 'Mary Shelley');

   Look at projects/library_example/seed.sql for a finished example.
   Write your INSERT statements below this line.
   ========================================================================== */

