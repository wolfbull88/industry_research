#!/bin/bash
# 竞争对手及行业新闻追踪脚本
# 使用: ./fetch_news.sh

DATA_DIR="/home/wolfbull/.openclaw/workspace-mars/projects/industry_research/data"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

mkdir -p "$DATA_DIR"

echo "=== Fetching Competitor & Industry News ==="
echo "Timestamp: $TIMESTAMP"
echo ""

# Bolt
echo "[1/7] Bolt..."
curl -sL "https://bolt.eu/en/blog/" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE '/blog/[^"]+' | grep -v "category" | sort -u | head -10 > "$DATA_DIR/bolt_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/bolt_$TIMESTAMP.txt") articles"

# Dott
echo "[2/7] Dott..."
curl -sL "https://ridedott.com/press-release/" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE '/press-release/[^"]+' | grep -v "page/" | grep -v "breadcrumb" | sort -u | head -10 > "$DATA_DIR/dott_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/dott_$TIMESTAMP.txt") articles"

# Donkey Republic
echo "[3/7] Donkey Republic..."
curl -sL "https://www.donkey.bike/blog" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="/blogs/[^"]*"' | sed 's/href="//;s/"//' | sort -u > "$DATA_DIR/donkey_republic_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/donkey_republic_$TIMESTAMP.txt") articles"

# Voi
echo "[4/7] Voi..."
curl -sL "https://www.voiscooters.com" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE '"slug":"[^"]+"' | grep -v "slug\":\"index" | head -10 > "$DATA_DIR/voi_$TIMESTAMP.txt"
echo "  Found content"

# Ryde
echo "[5/7] Ryde..."
curl -sL "https://www.ryde-technology.com/blog" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="/blog/[^"]*"' | sort -u | head -10 > "$DATA_DIR/ryde_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/ryde_$TIMESTAMP.txt") articles"

# Zag Daily (行业媒体)
echo "[6/7] Zag Daily..."
curl -sL "https://zagdaily.com" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="https://zagdaily.com/[^"]*"' | head -20 > "$DATA_DIR/zagdaily_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/zagdaily_$TIMESTAMP.txt") links"

echo "[7/7] TechCrunch Micromobility..."
curl -sL "https://techcrunch.com/tag/micromobility/" -A "Mozilla/5.0" 2>/dev/null | \
  grep -oE 'href="https://techcrunch.com/[0-9]{4}/[0-9]{2}/[^"]*"' | head -10 > "$DATA_DIR/techcrunch_$TIMESTAMP.txt"
echo "  Found $(wc -l < "$DATA_DIR/techcrunch_$TIMESTAMP.txt") articles"

echo ""
echo "=== Done ==="
echo "Files saved to: $DATA_DIR"
ls -la "$DATA_DIR/*_$TIMESTAMP.txt" 2>/dev/null | tail -5
