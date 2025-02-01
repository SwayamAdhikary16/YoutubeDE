import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

# YouTube API endpoint for video details
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
# Get the YouTube API key from environment variables
YT_API_KEY = os.getenv('YT_API')

def fetch_video_data_numbers(video_id):
    """
    Fetches video statistics and snippet information for a given video ID.
    
    Args:
        video_id (str): The ID of the YouTube video.
    
    Returns:
        dict: A dictionary containing video title, channel, views, likes, and comments count.
    """
    # Parameters for the API request
    params = {
        "part": "statistics,snippet",
        "id": video_id,
        "key": YT_API_KEY,
    }

    # Send GET request to fetch video data
    response = requests.get(YOUTUBE_VIDEO_URL, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
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
                "comments": stats.get("commentCount", "N/A")
            }
        else:
            return {"Error": "Video not found"}
    else:
        return {"Error": [response.status_code, response.text]}

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

        # Send GET request to fetch comments
        response_comments = requests.get(YOUTUBE_COMMENTS_URL, params=params_comments)

        # Check if the response for comments is successful
        if response_comments.status_code == 200:
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
        else:
            return {"Error": [response_comments.status_code, response_comments.text]}

    # Clean the comments
    comments_df = pd.DataFrame(comments, columns=["Comment"])
    comments_df["CleanedComment"] = comments_df["Comment"].str.lower()
    comments_df["CleanedComment"] = comments_df["CleanedComment"].str.replace("[^a-zA-Z0-9\s]", "", regex=True)

    return {"comments": comments_df["CleanedComment"].tolist()}
