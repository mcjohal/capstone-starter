# YOUR project's names and labels. Fill these in during Part 4, Step 2 of
# the guide (docs/04-write-your-sql.md). Change only the text inside the
# quotes. projects/library_example/settings.py shows every one filled in.

SITE_NAME = "My Capstone Project"            # the name at the top of every page
TAGLINE = "One sentence about what this site keeps track of."
ICON = "database"                            # any icon name from icons.getbootstrap.com

YOUR_NAME = "Your Name"
COURSE = "CIS 4720"                          # or CIS 2020
GITHUB_URL = ""                              # your repository address, once you have one

# What one row on the Browse page is called, for example "recipe" and "recipes"
ITEM = "item"
ITEMS = "items"

BROWSE_TITLE = "All items"
BROWSE_INTRO = "Every item, in order. Click one to see its details."

DETAIL_RELATED_TITLE = "Related rows"
DETAIL_RELATED_EMPTY = "Nothing related to this one yet."

SEARCH_HINT = "Search by name"

REPORT_TITLE = "Summary"
REPORT_INTRO = "One sentence about what this report counts or averages."

ADD_TITLE = "Add an item"

# One entry for each box on the Add page, in the order they should appear.
# The name must match a placeholder in queries/add.sql (name "title" fills
# :title). Leave this list empty until you reach Step 11 of Part 4.
#
#   type "text"    a text box
#   type "number"  a number box
#   type "date"    a date picker, saved as YYYY-MM-DD
#   type "select"  a dropdown, filled by the query file named in "options"
#
# Example, from the library:
#   ADD_FORM = [
#       {"name": "title", "label": "Title", "type": "text", "required": True},
#       {"name": "author_id", "label": "Author", "type": "select",
#        "options": "queries/add_options.sql", "required": True},
#       {"name": "pages", "label": "Pages", "type": "number"},
#   ]
ADD_FORM = []
