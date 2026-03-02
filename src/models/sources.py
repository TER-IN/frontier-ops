import yaml
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

class Source(BaseModel):
    id: str
    type: str # youtube_channel, rss_feed, subreddit, twitter_list
    url: str
    trust_weight: float
    frequency: str
    description: Optional[str] = None

def load_sources(file_path: str = "data/SOURCES.yml") -> List[Source]:
    """Loads the curated list of high-signal sources from YAML."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Sources file not found at {file_path}")
        
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    sources = []
    for src_data in data.get("sources", []):
        sources.append(Source(**src_data))
        
    return sources

if __name__ == "__main__":
    sources = load_sources()
    print(f"Loaded {len(sources)} sources to monitor:")
    for src in sources:
        print(f"- {src.id} ({src.type})")
