#!/usr/bin/env python3
"""Post generated CEE Spring stats to the Wikipedia statistics page.

Usage:
    uv run python post_stats.py              # post output/cee_spring_2026_results.txt
    uv run python post_stats.py --dry-run    # print what would be posted without editing
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from src.config import OUTPUT_FILE
from src.wikipedia_poster import WikipediaPoster

load_dotenv()

STATS_PAGE = "Vikipēdija:CEE Spring 2026/Statistika"
BEGIN_MARKER = os.environ.get("WIKI_BEGIN_MARKER", "<!-- BEGIN -->")
END_MARKER = os.environ.get("WIKI_END_MARKER", "<!-- END -->")
EDIT_SUMMARY = "Automātisks CEE Spring 2026 statistikas atjauninājums"


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
    args = parser.parse_args()

    # Read the generated stats
    if not os.path.exists(args.file):
        print(f"Results file not found: {args.file}")
        print("Run 'uv run python cee_spring_stats.py' first to generate stats.")
        return 1

    with open(args.file, encoding="utf-8") as f:
        new_stats = f.read()

    if args.dry_run:
        print(f"--- Would post to: {STATS_PAGE} ---")
        print(f"Begin marker: {BEGIN_MARKER!r}")
        print(f"End marker:   {END_MARKER!r}")
        print(f"Content ({len(new_stats)} chars):")
        print(new_stats[:500] + ("..." if len(new_stats) > 500 else ""))
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

    success = poster.update_between_markers(
        title=STATS_PAGE,
        new_content=new_stats,
        begin_marker=BEGIN_MARKER,
        end_marker=END_MARKER,
        summary=EDIT_SUMMARY,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
