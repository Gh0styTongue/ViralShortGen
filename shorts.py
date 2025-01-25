import os
import json
import random
from googleapiclient.discovery import build

API_KEY = "YOUR_GOOGLE_API_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
EXCLUDED_CATEGORIES = {"10", "30"}
FEEDBACK_FILE = "feedback.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return {"good": [], "bad": []}

def save_feedback(feedback):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f, indent=4)

def get_trending_videos(api_key, max_results=50, page_token=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=max_results,
        regionCode="US",
        pageToken=page_token
    )
    return request.execute()

def parse_duration(duration):
    time = {"H": 0, "M": 0, "S": 0}
    for unit in time.keys():
        if f"{unit}" in duration:
            value = duration.split(f"{unit}")[0].split("T")[-1].split("H")[-1].split("M")[-1]
            time[unit] = int(value)
            duration = duration.replace(f"{value}{unit}", "")
    return time["H"] * 3600 + time["M"] * 60 + time["S"]

def generate_short(video, feedback, min_length=15, max_length=60):
    duration = video["duration"]
    previous_good = [f for f in feedback["good"] if f["video_id"] == video["id"]]
    previous_bad = [f for f in feedback["bad"] if f["video_id"] == video["id"]]

    if previous_good:
        start_time = random.choice(previous_good)["start_time"]
        short_duration = random.choice(previous_good)["duration"]
    else:
        start_time = random.randint(0, max(0, duration - max_length))
        short_duration = random.randint(min_length, min(max_length, duration - start_time))
        while any(bad["start_time"] == start_time and bad["duration"] == short_duration for bad in previous_bad):
            start_time = random.randint(0, max(0, duration - max_length))
            short_duration = random.randint(min_length, min(max_length, duration - start_time))

    short_url = f"https://www.youtube.com/watch?v={video['id']}&t={start_time}s"
    return {
        "video_id": video["id"],
        "title": video["title"],
        "channel": video["channel"],
        "short_url": short_url,
        "start_time": start_time,
        "duration": short_duration
    }

def collect_feedback(short):
    print(f"\nGenerated Short:")
    print(f"Title: {short['title']}")
    print(f"Channel: {short['channel']}")
    print(f"Short URL: {short['short_url']}")
    print(f"Start Time: {short['start_time']} seconds")
    print(f"Duration: {short['duration']} seconds")
    response = input("Is this good? [yes/no]: ").strip().lower()
    return response == "yes"

def main():
    feedback = load_feedback()
    shorts = []
    next_page_token = None

    while len(shorts) < 5:
        trending_videos_data = get_trending_videos(API_KEY, page_token=next_page_token)
        trending_videos = [
            {
                "id": item["id"],
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "duration": parse_duration(item["contentDetails"]["duration"])
            }
            for item in trending_videos_data.get("items", [])
            if item["snippet"]["categoryId"] not in EXCLUDED_CATEGORIES and parse_duration(item["contentDetails"]["duration"]) >= 60
        ]

        next_page_token = trending_videos_data.get("nextPageToken")

        for video in trending_videos:
            if any(f["video_id"] == video["id"] for f in feedback["good"] + feedback["bad"]):
                continue
            short = generate_short(video, feedback)
            is_good = collect_feedback(short)
            if is_good:
                feedback["good"].append({
                    "video_id": short["video_id"],
                    "start_time": short["start_time"],
                    "duration": short["duration"]
                })
                shorts.append(short)
            else:
                feedback["bad"].append({
                    "video_id": short["video_id"],
                    "start_time": short["start_time"],
                    "duration": short["duration"]
                })
            save_feedback(feedback)
            if len(shorts) >= 5:
                break

        if not next_page_token:
            break

    print("\nSummary of Shorts:")
    for short in shorts:
        print(f"- {short['title']} ({short['duration']}s): {short['short_url']}")

    more = input("\nGenerate more shorts? [yes/no]: ").strip().lower()
    if more == "yes":
        main()

if __name__ == "__main__":
    main()
