#!/bin/bash
# Micromobility.io News Scraper
# Fetches recent news articles from micromobility.io

DATA_DIR="/home/wolfbull/.openclaw/workspace-mars/projects/industry_research/data"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

mkdir -p "$DATA_DIR"

echo "=== Fetching Micromobility.io News ==="

# Fetch news list
curl -sL "https://micromobility.io/news" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="/news/[^"]*"' | \
  sed 's/href="//;s/"//' | \
  sort -u > "$DATA_DIR/micromobility_io_$TIMESTAMP.txt"

echo "Found $(wc -l < "$DATA_DIR/micromobility_io_$TIMESTAMP.txt") articles"

# Show first 10
echo ""
echo "Recent articles:"
head -10 "$DATA_DIR/micromobility_io_$TIMESTAMP.txt"

echo ""
echo "=== Done ==="
