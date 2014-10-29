"""This input filter will filter out certain blog posts based on the <category>
element.

This is not totally dissimilar to the function of the xpath_sifter.py plugin.
The main difference are that this one uses minidom instead of xpath and instead
of using global requires and excludes, this plugin looks for a feed-level
configuration parameter called filter_categories, which is a comma-separated
list of categories that are allowed.  If at least one of the categories is not
found in the blog entry then the entry is rejected.
"""

import sys
from xml.dom import minidom

entry = sys.stdin.read()
entry_dom = minidom.parseString(entry)
filter_data = entry_dom.getElementsByTagName("planet:filter_categories")

# If a configuration parameter called filter_categories exists then grab it's
# contents and proceed, otherwise allow the entry and exit
if filter_data:
    filter_categories = filter_data[0].firstChild.data.strip()
else:
    sys.stdout.write(entry)
    sys.exit(0)

# Break up the comma-separated category list into a list
categories = [cat.strip().lower() for cat in filter_categories.split(',')]

# Collect all the <category> elements from the entry and then see
# if it also happens to be in our required categories list.  If there aren't
# any <category> elements in the entry then skip it
entry_categories = entry_dom.getElementsByTagName('category')
if len(entry_categories) > 0:
    for entry_category in entry_categories:
        if entry_category.attributes['term'].value.lower() in categories:
            sys.stdout.write(entry)
            sys.exit(0)
else:
    sys.exit(1)

# By default we reject the entry
sys.exit(1)
