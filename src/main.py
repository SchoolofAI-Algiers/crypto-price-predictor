import os
import sys

params = {}

if len(sys.argv) >= 2:
    params["query"] = sys.argv[1]
else:
    params["query"] = input("Enter the query\n")

if len(sys.argv) >= 3:
    params["language"] = sys.argv[2]
else:
    params["language"] = "en"

os.environ['QUERY'] = params["query"]
os.environ['LANGUAGE'] = params["language"]

import scraper

scraper.main()
