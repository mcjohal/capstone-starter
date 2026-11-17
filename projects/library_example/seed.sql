/* ==========================================================================
   seed.sql   Valley Library (the example)
   The sample rows. The app runs this right after schema.sql.
   Parent rows go first: an author must exist before a book points at it,
   and a book and a member must exist before a loan points at them.
   ========================================================================== */

-- authors. The ids are given so the books below can point at them.
INSERT INTO authors (author_id, name, country, born_year) VALUES
    (1,  'Jane Austen',          'England',        1775),
    (2,  'Mary Shelley',         'England',        1797),
    (3,  'Mark Twain',           'United States',  1835),
    (4,  'Jules Verne',          'France',         1828),
    (5,  'Arthur Conan Doyle',   'Scotland',       1859),
    (6,  'Louisa May Alcott',    'United States',  1832),
    (7,  'H. G. Wells',          'England',        1866),
    (8,  'Charles Dickens',      'England',        1812),
    (9,  'Herman Melville',      'United States',  1819),
    (10, 'Charlotte Bronte',     'England',        1816);

-- books. author_id must match a row above.
INSERT INTO books (book_id, title, author_id, genre, year_published, pages) VALUES
    (1,  'Pride and Prejudice',                    1,  'Romance',          1813, 432),
    (2,  'Emma',                                   1,  'Romance',          1815, 474),
    (3,  'Frankenstein',                           2,  'Horror',           1818, 280),
    (4,  'The Adventures of Tom Sawyer',           3,  'Adventure',        1876, 274),
    (5,  'Adventures of Huckleberry Finn',         3,  'Adventure',        1884, 366),
    (6,  'Twenty Thousand Leagues Under the Seas', 4,  'Science Fiction',  1870, 426),
    (7,  'Around the World in Eighty Days',        4,  'Adventure',        1872, 256),
    (8,  'The Hound of the Baskervilles',          5,  'Mystery',          1902, 256),
    (9,  'A Study in Scarlet',                     5,  'Mystery',          1887, 188),
    (10, 'Little Women',                           6,  'Classic',          1868, 449),
    (11, 'The Time Machine',                       7,  'Science Fiction',  1895, 118),
    (12, 'The War of the Worlds',                  7,  'Science Fiction',  1898, 192),
    (13, 'A Tale of Two Cities',                   8,  'Classic',          1859, 489),
    (14, 'Moby Dick',                              9,  'Adventure',        1851, 635),
    (15, 'Jane Eyre',                              10, 'Romance',          1847, 532);

-- members
INSERT INTO members (member_id, name, email, joined_on) VALUES
    (1,  'Ana Lopez',       'ana.lopez@example.com',       '2025-01-15'),
    (2,  'Ben Carter',      'ben.carter@example.com',      '2025-02-03'),
    (3,  'Chloe Nguyen',    'chloe.nguyen@example.com',    '2025-03-22'),
    (4,  'David Singh',     'david.singh@example.com',     '2025-04-10'),
    (5,  'Elena Garcia',    'elena.garcia@example.com',    '2025-05-05'),
    (6,  'Frank Miller',    'frank.miller@example.com',    '2025-06-18'),
    (7,  'Grace Kim',       'grace.kim@example.com',       '2025-07-01'),
    (8,  'Hector Ramirez',  'hector.ramirez@example.com',  '2025-08-12'),
    (9,  'Isla Thompson',   'isla.thompson@example.com',   '2025-09-30'),
    (10, 'Jamal Brooks',    'jamal.brooks@example.com',    '2025-10-14');

-- loans. returned_on is NULL for books that are still checked out.
INSERT INTO loans (book_id, member_id, loaned_on, returned_on) VALUES
    (1,  1,  '2026-01-05', '2026-01-19'),
    (3,  2,  '2026-01-08', '2026-01-25'),
    (8,  3,  '2026-01-12', '2026-01-20'),
    (1,  4,  '2026-02-01', '2026-02-14'),
    (11, 5,  '2026-02-03', '2026-02-10'),
    (14, 6,  '2026-02-15', '2026-03-20'),
    (5,  7,  '2026-03-02', '2026-03-16'),
    (8,  8,  '2026-03-10', '2026-03-18'),
    (15, 9,  '2026-03-25', '2026-04-15'),
    (1,  10, '2026-04-02', '2026-04-20'),
    (12, 2,  '2026-04-11', '2026-04-22'),
    (10, 3,  '2026-05-01', NULL),
    (6,  1,  '2026-05-06', NULL),
    (8,  5,  '2026-05-09', NULL),
    (13, 7,  '2026-05-12', NULL);
