#!/bin/bash
# 竞争对手新闻追踪脚本
# 使用: ./fetch_competitors.sh

DATA_DIR="/home/wolfbull/.openclaw/workspace-mars/projects/industry_research/data"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

mkdir -p "$DATA_DIR"

echo "=== Fetching Competitor News ==="
echo "Timestamp: $TIMESTAMP"
echo ""

# Donkey Republic
echo "Fetching Donkey Republic..."
curl -sL "https://www.donkey.bike/blog" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="/blogs/[^"]*"' | sed 's/href="//;s/"//' | sort -u > "$DATA_DIR/donkey_republic_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/donkey_republic_$TIMESTAMP.txt") articles"

# Voi
echo "Fetching Voi..."
curl -sL "https://www.voiscooters.com" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE '"slug":"[^"]+"' | head -10 > "$DATA_DIR/voi_$TIMESTAMP.txt"
echo "  Found content"

# Lime (try main page)
echo "Fetching Lime..."
curl -sL "https://www.li.me" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="[^"]*"' | grep -i "blog\|news\|press" | head -10 > "$DATA_DIR/lime_$TIMESTAMP.txt" 2>/dev/null
echo "  Done"

# Bolt
echo "Fetching Bolt..."
curl -sL "https://bolt.eu/news/" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="[^"]*"' | grep -i "news\|blog" | head -10 > "$DATA_DIR/bolt_$TIMESTAMP.txt" 2>/dev/null
echo "  Done"

echo ""
echo "=== Done ==="
ls -la "$DATA_DIR"
