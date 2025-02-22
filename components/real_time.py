import sys
import os 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import youtube_api as yt

def get_real_time_data(video_id):
    data = yt.fetch_video_data(video_id)

    if not data:
       return {"error":"No data found"}
    return {
      "views":data['viewCount'],
      "likes":data['likeCount'],
      "comments":data['commentCount']
    }

