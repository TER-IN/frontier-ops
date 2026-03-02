import json
from pathlib import Path
from typing import List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# We need a way to get the latest videos from a channel.
# In a full production system, we'd use the YouTube Data API v3.
# For this MVP, we will assume we are given video IDs directly or 
# we can use a library like yt-dlp to list videos. 
# For now, let's implement the core transcript extraction given a video ID.

def extract_video_id(url: str) -> Optional[str]:
    """Extracts the video ID from a standard YouTube URL."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def fetch_transcript(video_id: str) -> Optional[str]:
    """Fetches the english transcript for a given YouTube video ID."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id).find_transcript(['en']).fetch()
        formatter = TextFormatter()
        return formatter.format_transcript(transcript_list)
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def save_transcript(video_id: str, transcript: str, output_dir: str = "data/raw/youtube"):
    """Saves the raw transcript to the ingestion folder."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    
    file_path = path / f"{video_id}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Saved transcript to {file_path}")

if __name__ == "__main__":
    # Test with a known AI engineering video (e.g., from AI Engineer channel)
    # E.g. "Building a multi-agent system"
    test_video_url = "https://www.youtube.com/watch?v=RnjgLlQTMf0" # The Frontier Ops video
    print(f"Testing ingestion on: {test_video_url}")
    
    vid_id = extract_video_id(test_video_url)
    if vid_id:
        transcript = fetch_transcript(vid_id)
        if transcript:
            print(f"Successfully fetched {len(transcript)} characters of transcript.")
            save_transcript(vid_id, transcript)
        else:
            print("Failed to fetch transcript.")
    else:
        print("Invalid URL")
