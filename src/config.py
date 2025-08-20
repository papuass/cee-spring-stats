"""Configuration settings for the Wikipedia statistics tool."""

import os
from dotenv import load_dotenv

load_dotenv()

# MediaWiki API settings
MEDIAWIKI_API_URL = "https://lv.wikipedia.org/w/api.php"
META_WIKI_API_URL = "https://meta.wikimedia.org/w/api.php"
USER_AGENT = "CEE-Spring-Stats-Tool/1.0 (https://lv.wikipedia.org/wiki/User:YourUsername)"

# Contest settings
CONTEST_YEAR = "2025"
CONTEST_TEMPLATE = f"CEE Spring {CONTEST_YEAR}"
STRUCTURE_PAGE_PREFIX = f"Wikimedia CEE Spring {CONTEST_YEAR}/Structure/"
CATEGORY_PREFIX = f"CEE Spring {CONTEST_YEAR} raksti"

# API rate limiting (requests per second)
API_RATE_LIMIT = 1.0

# Output settings
OUTPUT_FILE = f"output/cee_spring_{CONTEST_YEAR}_results.txt"
CACHE_FILE = f"cache/cee_spring_{CONTEST_YEAR}_cache.json"

# No limits on topics and countries - parse and display all

# Contest countries configuration
# Only these countries are counted in contest categories
ALLOWED_CONTEST_COUNTRIES = [
    "Albānija", "Armēnija", "aromūni", "Austrija", "Azerbaidžāna",
    "Baltkrievija", "Baškortostāna", "Bosnija un Hercegovina", "Bulgārija",
    "Čehija", "čigāni", "Čuvašija", "erzji", "esperanto", "Grieķija",
    "Gruzija", "Horvātija", "Igaunija", "karaīmi", "Kazahstāna", "Kipra",
    "Kosova", "Krievija", "Krievijas ziemeļrietumu reģions", "Krimas tatāri",
    "krimčaki", "Lietuva", "Malta", "Melnkalne", "Polija",
    "rietumarmēņu valoda", "Rumānija un Moldova", "Serbija", "Serbu Republika",
    "Slovākija", "Slovēnija", "sorbi", "starptautiski", "tatāri", "Turcija",
    "Ukraina", "Ungārija", "veru valoda", "Ziemeļmaķedonija"
]