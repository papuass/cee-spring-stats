#!/usr/bin/env python3
"""Post generated CEE Spring stats to the Wikipedia statistics and results pages.

Usage:
    uv run python post_stats.py              # post stats and contest categories
    uv run python post_stats.py --dry-run    # print what would be posted without editing
"""

import argparse
import os
import re
import sys
from dotenv import load_dotenv

from src.config import OUTPUT_FILE
from src.wikipedia_poster import WikipediaPoster

load_dotenv()

STATS_PAGE = "Vikipēdija:CEE Spring 2026/Statistika"
RESULTS_PAGE = "Vikipēdija:CEE Spring 2026/Rezultāti"
CATEGORIES_FILE = "output/contest_categories.txt"
BEGIN_MARKER = os.environ.get("WIKI_BEGIN_MARKER", "<!-- BEGIN -->")
END_MARKER = os.environ.get("WIKI_END_MARKER", "<!-- END -->")
EDIT_SUMMARY_STATS = "Automātisks CEE Spring 2026 statistikas atjauninājums"
EDIT_SUMMARY_RESULTS = "Automātisks CEE Spring 2026 rezultātu atjauninājums"


def main() -> int:
    """Entry point. Returns exit code."""
    parser = argparse.ArgumentParser(description="Post CEE Spring stats to Wikipedia")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the content that would be posted without actually editing",
    )
    parser.add_argument(
        "--file",
        default=OUTPUT_FILE,
        help=f"Path to results file (default: {OUTPUT_FILE})",
    )
    parser.add_argument(
        "--categories-file",
        default=CATEGORIES_FILE,
        help=f"Path to contest categories file (default: {CATEGORIES_FILE})",
    )
    args = parser.parse_args()

    # Read the generated stats
    if not os.path.exists(args.file):
        print(f"Results file not found: {args.file}")
        print("Run 'uv run python cee_spring_stats.py' first to generate stats.")
        return 1

    with open(args.file, encoding="utf-8") as f:
        new_stats = f.read()

    match = re.search(r"Kopējais rakstu skaits:'''\s*(\d+)", new_stats)
    article_count = match.group(1) if match else "?"
    edit_summary_stats = f"{EDIT_SUMMARY_STATS} ({article_count} raksti)"

    # Read the contest categories
    if not os.path.exists(args.categories_file):
        print(f"Categories file not found: {args.categories_file}")
        print("Run 'uv run python cee_spring_stats.py' first to generate stats.")
        return 1

    with open(args.categories_file, encoding="utf-8") as f:
        new_categories = f.read()

    if args.dry_run:
        print(f"Edit summary: {edit_summary_stats}")
        print(f"--- Would post to: {STATS_PAGE} ---")
        print(f"Begin marker: {BEGIN_MARKER!r}")
        print(f"End marker:   {END_MARKER!r}")
        print(f"Content ({len(new_stats)} chars):")
        print(new_stats[:500] + ("..." if len(new_stats) > 500 else ""))
        print()
        print(f"--- Would post to: {RESULTS_PAGE} ---")
        print(f"Begin marker: {BEGIN_MARKER!r}")
        print(f"End marker:   {END_MARKER!r}")
        print(f"Content ({len(new_categories)} chars):")
        print(new_categories[:500] + ("..." if len(new_categories) > 500 else ""))
        return 0

    # Check credentials
    username = os.environ.get("WIKI_USERNAME")
    password = os.environ.get("WIKI_PASSWORD")

    if not username or not password:
        print(
            "Error: WIKI_USERNAME and WIKI_PASSWORD must be set in .env\n"
            "Create a bot password at https://lv.wikipedia.org/wiki/Special:BotPasswords"
        )
        return 1

    poster = WikipediaPoster()

    if not poster.login(username, password):
        return 1

    success_stats = poster.update_between_markers(
        title=STATS_PAGE,
        new_content=new_stats,
        begin_marker=BEGIN_MARKER,
        end_marker=END_MARKER,
        summary=edit_summary_stats,
    )

    success_results = poster.update_between_markers(
        title=RESULTS_PAGE,
        new_content=new_categories,
        begin_marker=BEGIN_MARKER,
        end_marker=END_MARKER,
        summary=EDIT_SUMMARY_RESULTS,
    )

    return 0 if (success_stats and success_results) else 1


if __name__ == "__main__":
    sys.exit(main())
