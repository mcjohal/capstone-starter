# Names and labels for the library example. Your own copy of this file is
# projects/my_project/settings.py. Text goes inside quotes.

SITE_NAME = "Valley Library"
TAGLINE = "A small public library catalog of books, authors, members, and loans."
ICON = "book"                       # any icon name from icons.getbootstrap.com

YOUR_NAME = "Library Example"
COURSE = "Capstone Project"
GITHUB_URL = ""                     # your repository address, once you have one

# What one row on the Browse page is called
ITEM = "book"
ITEMS = "books"

BROWSE_TITLE = "All books"
BROWSE_INTRO = "Every book in the catalog, newest first. Click a title to see its details and loan history."

DETAIL_RELATED_TITLE = "Loan history"
DETAIL_RELATED_EMPTY = "This book has never been borrowed."

SEARCH_HINT = "Search by title, author, or genre"

REPORT_TITLE = "Books by genre"
REPORT_INTRO = "How many books the library has in each genre, and how long they are on average."

ADD_TITLE = "Add a book"

# One entry for each box on the Add page. The name must match a
# placeholder in queries/add.sql (name "title" fills :title).
#   type "text"    a text box
#   type "number"  a number box
#   type "date"    a date picker, saved as YYYY-MM-DD
#   type "select"  a dropdown filled by the query file named in "options"
ADD_FORM = [
    {"name": "title", "label": "Title", "type": "text", "required": True},
    {"name": "author_id", "label": "Author", "type": "select", "options": "queries/add_author_options.sql",
     "required": True},
    {"name": "genre", "label": "Genre", "type": "text"},
    {"name": "year_published", "label": "Year published", "type": "number"},
    {"name": "pages", "label": "Pages", "type": "number"},
]
