import os 
from dotenv import load_dotenv
import requests

load_dotenv()
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YT_API_KEY = os.getenv('YT_API')

def fetch_video_data_numbers(video_id):
    
    params = {
    "part": "statistics,snippet",
    "id": video_id,
    "key": YT_API_KEY,
    }

    response = requests.get(YOUTUBE_VIDEO_URL, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            video_data = data["items"][0]
            stats = video_data["statistics"]

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
        return {"Error:":[response.status_code, response.text]}
    
def fetch_video_comments(video_id):
    
    # YouTube API endpoint for comments
    YOUTUBE_COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

    # API parameters for fetching comments
    params_comments = {
        "part": "snippet",
        "videoId": video_id,
        "key": YT_API_KEY,
        "maxResults": 10000,
        "order": "time",
    }

    # Send GET request to fetch comments
    response_comments = requests.get(YOUTUBE_COMMENTS_URL, params=params_comments)

    # Check if the response for comments is successful
    if response_comments.status_code == 200:
        data_comments = response_comments.json()
        comments = []
        if "items" in data_comments:
            print("\nRecent Comments:")
            for i, item in enumerate(data_comments["items"], start=1):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
        else:
            print("No comments found.")
        return {"comments": comments}
    else:
        return {"Error:", response_comments.status_code, response_comments.text}

if __name__ == "__main__":
    video_id = "sF5LYGgKbUA"
    print(fetch_video_data_numbers(video_id))
    print(fetch_video_comments(video_id))