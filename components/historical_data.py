import sys
import time
from datetime import datetime, timedelta
import queue
import os
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.youtube_api import fetch_video_data_numbers

# Queue to store real-time video data
data_queue = queue.Queue()

# Store historical data for the last 1 hour
historical_data = {
    "timestamps": [],
    "views": [],
    "likes": [],
    "comments": []
}

# API Constants
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YT_API_KEY = os.getenv('YT_API_KEY')


def update_historical_data(video_id):
    """
    Fetches real-time video stats and stores them in historical data (last 1 hour).
    """
    video_stats = fetch_video_data_numbers(video_id)

    if "Error" not in video_stats:
        # Append new data
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historical_data["timestamps"].append(now)
        historical_data["views"].append(video_stats["views"])
        historical_data["likes"].append(video_stats["likes"])
        historical_data["comments"].append(video_stats["comments"])

        # Remove old data (beyond 1 hour)
        cutoff_time = datetime.now() - timedelta(hours=1)
        while historical_data["timestamps"] and datetime.strptime(historical_data["timestamps"][0], "%Y-%m-%d %H:%M:%S") < cutoff_time:
            historical_data["timestamps"].pop(0)
            historical_data["views"].pop(0)
            historical_data["likes"].pop(0)
            historical_data["comments"].pop(0)

        print(f"{historical_data}")
    else:
        print(f"Error fetching video data: {video_stats['Error']}")

def get_historical_data(video_id):
    """
    Returns the stored historical data for visualization.
    """
    for _ in range(5):
        update_historical_data(video_id)
        time.sleep(60)
    return historical_data

if __name__ == "__main__":
    video_id = "sF5LYGgKbUA"

    # Simulating real-time updates (every minute for 5 minutes)
    for _ in range(5):
        update_historical_data(video_id)
        time.sleep(60)  # Wait 1 minute before next update

    # Get the stored historical data
    print(get_historical_data())
