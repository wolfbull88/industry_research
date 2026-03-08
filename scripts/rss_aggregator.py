#!/usr/bin/env python3
"""
RSS + Web Aggregator for Micromobility Industry News
- Filters for micromobility-related content only
- Fetches all articles from past 7 days
Usage: python3 rss_aggregator.py
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import html
import re
import json
import os

# Keywords to filter for micromobility
MICROMOBILITY_KEYWORDS = [
    'micromobility', 'e-scooter', 'escooter', 'electric scooter',
    'e-bike', 'ebike', 'electric bike', 'e-bikes', 'ebikes',
    'shared scooter', 'shared bike', 'shared mobility',
    'lime', 'voi', 'bolt', 'dott', 'tier', 'bird', 'spin',
    'ridemovi', 'donkey', 'ryde', 'nextbike',
    'scooter sharing', 'bike sharing', 'dockless',
    'vehiclesharing', 'micro-mobility', 'micromobil',
    'electric vehicle', 'emobility', 'e-mobility',
    'urban mobility', 'last mile', 'last-mile',
    'city bike', 'velib', 'bixi',
]

# RSS Feed URLs
RSS_FEEDS = {
    "Zag Daily": {
        "url": "https://zagdaily.com/feed/",
    },
    "Micromobility Substack": {
        "url": "https://micromobility.substack.com/feed",
    },
    "Fluctuo": {
        "url": "https://blog.fluctuo.com/rss/",
    },
    "Electrek": {
        "url": "https://electrek.co/feed/",
    },
    "TechCrunch": {
        "url": "https://techcrunch.com/tag/micromobility/feed/",
    },
}

# File to store previously reported articles (for deduplication)
HISTORY_FILE = "/home/wolfbull/.openclaw/workspace-mars/projects/industry_research/data/reported_articles.json"

def is_relevant(title, description):
    """Check if article is micromobility related"""
    text = (title + " " + (description or "")).lower()
    
    for keyword in MICROMOBILITY_KEYWORDS:
        if keyword.lower() in text:
            return True
    return False

def parse_date(date_str):
    """Parse various date formats"""
    if not date_str:
        return None
    
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip()[:25], fmt.replace(' %z', ''))
        except:
            continue
    
    try:
        return datetime.strptime(date_str[:16], '%a, %d %b %Y')
    except:
        return None

def fetch_rss(feed_name, url, days_back=7):
    """Fetch and parse RSS feed with filtering"""
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode('utf-8')
        
        root = ET.fromstring(content)
        items = []
        
        for item in root.findall('.//item'):
            title_elem = item.find('title')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            desc_elem = item.find('description')
            
            title = html.unescape(title_elem.text) if title_elem is not None else ""
            link = link_elem.text if link_elem is not None else ""
            pub_date_str = pub_date_elem.text if pub_date_elem is not None else ""
            description = html.unescape(desc_elem.text[:300]) if desc_elem is not None and desc_elem.text else ""
            
            pub_date = parse_date(pub_date_str)
            
            if not is_relevant(title, description):
                continue
            
            if pub_date and pub_date < cutoff_date:
                continue
            
            items.append({
                'title': title.strip(),
                'link': link.strip() if link else "",
                'pub_date': pub_date.strftime('%Y-%m-%d') if pub_date else pub_date_str[:16],
                'description': description.strip(),
                'source': feed_name
            })
        
        return items
    
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return []

def fetch_micromobility_io(days_back=7):
    """Fetch news from micromobility.io"""
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    try:
        url = "https://micromobility.io/news"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode('utf-8')
        
        items = []
        
        # Extract article links and dates
        # Pattern: href="/news/xxx" followed by date
        links = re.findall(r'href="(/news/[^"]+)"', content)
        dates = re.findall(r'>(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d+)', content)
        
        # Clean up and deduplicate
        unique_links = list(set(links))[:20]
        
        for i, link in enumerate(unique_links):
            full_url = f"https://micromobility.io{link}"
            title = link.replace('/news/', '').replace('-', ' ').title()
            
            # Try to get date from index
            pub_date_str = ""
            if i < len(dates):
                month = dates[i][0]
                day = dates[i][1]
                pub_date_str = f"2026-{month[:3]}-{int(day):02d}"
                try:
                    pub_date = datetime.strptime(pub_date_str, '%Y-%b-%d')
                except:
                    pub_date = None
            else:
                pub_date = None
            
            # Filter by date
            if pub_date and pub_date < cutoff_date:
                continue
            
            items.append({
                'title': title,
                'link': full_url,
                'pub_date': pub_date_str if pub_date_str else "2026-02",
                'description': "Micromobility.io News",
                'source': "Micromobility.io"
            })
        
        return items
    
    except Exception as e:
        print(f"  Error fetching micromobility.io: {e}")
        return []

def load_reported_articles():
    """Load previously reported article links from history file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('links', []))
        except:
            pass
    return set()

def save_reported_articles(news_items):
    """Save current article links to history file"""
    existing = load_reported_articles()
    for item in news_items:
        if item.get('link'):
            existing.add(item['link'])
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump({'links': list(existing)}, f)

def filter_duplicates(news_items):
    """Filter out articles that were already reported"""
    reported = load_reported_articles()
    original_count = len(news_items)
    filtered = [item for item in news_items if item.get('link') not in reported]
    removed = original_count - len(filtered)
    return filtered, removed

def main():
    print("=" * 70)
    print("🪐 Micromobility Industry News Aggregator")
    print("=" * 70)
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time range: Last 7 days")
    print(f"Filter: Micromobility-related only")
    print()
    
    all_news = []
    
    # RSS Feeds
    for name, config in RSS_FEEDS.items():
        url = config['url']
        print(f"📰 {name}...")
        
        items = fetch_rss(name, url, days_back=7)
        
        if items:
            print(f"   Found {len(items)} relevant articles")
            for item in items:
                all_news.append(item)
        else:
            print("   No relevant articles found")
    
    # Micromobility.io
    print(f"📰 Micromobility.io...")
    io_items = fetch_micromobility_io(days_back=7)
    if io_items:
        print(f"   Found {len(io_items)} articles")
        for item in io_items:
            all_news.append(item)
    else:
        print("   No articles found")
    
    # Filter duplicates (remove articles already reported in previous weeks)
    all_news, removed_count = filter_duplicates(all_news)
    if removed_count > 0:
        print(f"\n🗑️  Filtered {removed_count} duplicate articles (already in previous weeks)")
    
    # Save current articles to history for next week
    save_reported_articles(all_news)
    
    # Sort by date
    all_news.sort(key=lambda x: x['pub_date'] or "", reverse=True)
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTS: {len(all_news)} micromobility articles (last 7 days)")
    print("=" * 70)
    
    for i, news in enumerate(all_news, 1):
        print(f"\n{i}. [{news['source']}] {news['pub_date']}")
        print(f"   {news['title']}")
        print(f"   🔗 {news['link']}")
    
    # Save to file
    output_file = "/home/wolfbull/.openclaw/workspace-mars/projects/industry_research/data/rss_filtered.txt"
    with open(output_file, 'w') as f:
        f.write(f"Micromobility News - Last 7 Days\n")
        f.write(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, news in enumerate(all_news, 1):
            f.write(f"{i}. [{news['source']}] {news['pub_date']}\n")
            f.write(f"   {news['title']}\n")
            f.write(f"   {news['link']}\n\n")
    
    print(f"\n✅ Saved to: {output_file}")

if __name__ == "__main__":
    main()
