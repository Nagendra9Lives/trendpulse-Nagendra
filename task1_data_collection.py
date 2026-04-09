import requests
import time
import os
import json
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0"
categories = ["topstories", "newstories", "beststories", "askstories", "showstories"]

headers = {"User-Agent": "TrendPulse/1.0"}

all_stories = []

# Simple keyword-based category classifier
def classify_category(title):
    title = title.lower()

    if any(word in title for word in ["ai", "machine learning", "robot", "openai"]):
        return "AI"
    elif any(word in title for word in ["startup", "funding", "business"]):
        return "Business"
    elif any(word in title for word in ["python", "javascript", "code", "developer"]):
        return "Programming"
    else:
        return "General"


for category in categories:
    print(f"\nFetching {category}...\n")

    try:
        url = f"{BASE_URL}/{category}.json"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        ids = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch IDs for {category}: {e}")
        continue

    count = 0

    for story_id in ids:
        if count >= 25:   # Limit per category 
            break

        try:
            story_url = f"{BASE_URL}/item/{story_id}.json"
            res = requests.get(story_url, headers=headers)
            res.raise_for_status()
            story = res.json()

            # Skip if no title (safety)
            if not story or "title" not in story:
                continue

            processed = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": classify_category(story.get("title", "")),
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            all_stories.append(processed)
            count += 1

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Sleep AFTER each category loop
    print("Waiting 2 seconds...\n")
    time.sleep(2)


# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# File name with date
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

# Save to JSON
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_stories, f, indent=4)

# Final output
print(f"\nCollected {len(all_stories)} stories. Saved to {file_path}")