import feedparser
import json
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def fetch_rss_feed(feed_url: str):
    """Fetches and parses an RSS feed."""
    print(f"Fetching RSS feed: {feed_url}")
    feed = feedparser.parse(feed_url)
    
    entries = []
    for entry in feed.entries:
        # Extract plain text from HTML content if it exists
        content = entry.get('content', [{'value': entry.get('summary', '')}])[0]['value']
        soup = BeautifulSoup(content, 'html.parser')
        plain_text = soup.get_text(separator='\n', strip=True)
        
        # Parse published date
        published_parsed = entry.get('published_parsed')
        date_str = ""
        if published_parsed:
           dt = datetime(
               published_parsed[0], published_parsed[1], published_parsed[2],
               published_parsed[3], published_parsed[4], published_parsed[5],
               tzinfo=timezone.utc
           )
           date_str = dt.isoformat()
        
        entries.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': date_str,
            'content': plain_text
        })
    return entries

def save_rss_entries(source_id: str, entries: list, output_dir: str = "data/raw/rss"):
    """Saves the parsed RSS entries to JSON."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    
    # Create a safe filename using the source ID
    safe_name = "".join([c if c.isalnum() else "_" for c in source_id])
    file_path = path / f"{safe_name}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(entries)} RSS entries to {file_path}")

if __name__ == "__main__":
    # Test with Anthropic's research blog (if it has RSS, otherwise fallback)
    # Using a generic tech feed for testing if anthropic isn't available
    test_feed = "https://news.ycombinator.com/rss" 
    entries = fetch_rss_feed(test_feed)
    if entries:
        print(f"Successfully fetched {len(entries)} items. First item: {entries[0]['title']}")
        save_rss_entries("src_blog_hn_test", entries)
    else:
        print("Failed to fetch RSS feed.")
