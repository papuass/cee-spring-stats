#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting CEE Spring stats update"

cd "$PROJECT_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating stats..."
uv run python cee_spring_stats.py --no-cache

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Posting to Wikipedia..."
uv run python post_stats.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done"

curl -fsS --retry 3 https://hc-ping.com/b7d6a3c1-1ceb-4fee-92db-658be4e1cb00 > /dev/null
