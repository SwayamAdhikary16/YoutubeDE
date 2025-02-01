import os 
from dotenv import load_dotenv
import requests

load_dotenv()
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YT_API_KEY = os.getenv('YT_API')

def fetch_video_data_numbers(video_id):
    




