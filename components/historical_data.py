#real_time time series data {views,likes,comments,time}import queue
import time
import requests
import sys
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
# from utils.youtube_api import fetch_video_comments,fetch_video_data_numbers
# Create a queue to store the real-time video data
data_queue = queue.Queue()
import pandas as pd

# API Constants
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_COMMENT_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
YT_API_KEY=os.getenv('YT_API_KEY')
def fetch_video_data_numbers(video_id):
    
    # Parameters for the API request
    params = {
        "part": "statistics,snippet",
        "id": video_id,
        "key": YT_API_KEY,
    }

    try:
        # Send GET request to fetch video data
        response = requests.get(YOUTUBE_VIDEO_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"Error": str(e)}

    data = response.json()
    print(data)
    
    # Check if the video data is available
    if "items" in data and len(data["items"]) > 0:
        video_data = data["items"][0]
        stats = video_data["statistics"]
         
        # Return the relevant video data
        return {
            "title": video_data["snippet"]["title"],
            "channel": video_data["snippet"]["channelTitle"],
            "views": stats.get("viewCount", "N/A"),
            "likes": stats.get("likeCount", "N/A"),
            "comments": stats.get("commentCount", "N/A"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return {"Error": "Video not found"}
def fetch_video_comments(video_id, max_results=1000):
    """
    Fetches recent comments for a given video ID.
    
    Args:
        video_id (str): The ID of the YouTube video.
        max_results (int): The maximum number of comments to fetch.
    
    Returns:
        dict: A dictionary containing a list of cleaned comments or an error message.
    """
    # YouTube API endpoint for comments
    YOUTUBE_COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

    comments = []
    next_page_token = None

    while len(comments) < max_results:
        # API parameters for fetching comments
        params_comments = {
            "part": "snippet",
            "videoId": video_id,    
            "key": YT_API_KEY,
            "maxResults": min(max_results - len(comments), 100),
            "order": "time",
            "pageToken": next_page_token
        }

        try:
            # Send GET request to fetch comments
            response_comments = requests.get(YOUTUBE_COMMENTS_URL, params=params_comments)
            response_comments.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

        data_comments = response_comments.json()
        
        # Check if there are comments available
        if "items" in data_comments:
            for item in data_comments["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
        else:
            return {"Error": "No comments found."}
        
        next_page_token = data_comments.get("nextPageToken")
        if not next_page_token:
            break

    # Clean the comments
    comments_df = pd.DataFrame(comments, columns=["Comment"])
    comments_df["CleanedComment"] = comments_df["Comment"].str.lower()
   # comments_df["CleanedComment"] = comments_df["CleanedComment"].str.replace("[^a-zA-Z0-9\s]", "", regex=True)

    return {"comments": comments_df["CleanedComment"].tolist()}

def fetch_video_data(video_id):
    video_data = fetch_video_data_numbers(video_id)
    comments = fetch_video_comments(video_id)
    
    # Handle encoding issue
   # print(comments)  # Ensure Unicode support
    video_data["comments"] = comments["comments"]
    print()
   # print(video_data)
    data_queue.put(video_data)
    print(f"Data for video {video_id} stored in the queue")

def process_queue(video_id):
    while not data_queue.empty():
        video_data = data_queue.get()  # Get video data from the queue
        print(type(video_data))  # Check the type of the video data (should be a dict)
        data_queue.task_done()  # Mark the task as done
        return video_data  # 
    return None

#fetch_video_data("oPNWV5AGIQ8") # Replace with your video ID
#process_queue("oPNWV5AGIQ8")
