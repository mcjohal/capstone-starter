/* ==========================================================================
   schema.sql   YOUR TABLES                        (Part 4, Step 3 of the guide)
   The app runs this file first, every time it starts.

   Requirements
     * At least 3 tables, in third normal form.
     * Every table has a primary key:      some_id INTEGER PRIMARY KEY
     * At least 2 foreign keys linking the tables:
           FOREIGN KEY (author_id) REFERENCES authors(author_id)
     * Parent tables first. A table can only point at a table created
       above it.
     * CIS 4720 also: at least one CREATE VIEW and one CREATE TRIGGER,
       added at the bottom of this file in Part 4, Step 12.

   SQLite notes, if you are used to MySQL
     * INTEGER PRIMARY KEY numbers the rows for you. No AUTO_INCREMENT.
     * Use TEXT for words and dates (dates as 'YYYY-MM-DD'), INTEGER for
       whole numbers, REAL for decimals.
     * End every statement with a semicolon.

   Look at projects/library_example/schema.sql for a finished example.
   Write your CREATE TABLE statements below this line.
   ========================================================================== */

