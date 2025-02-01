from flask import Flask
from flask import jsonify,request
import requests
from utils.youtube_api import fetch_video_data_numbers,fetch_video_comments,get_video_id
from components.historical_data import fetch_video_data,process_queue
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/fetch_video_data', methods=['POST'])
def api_fetch_video_data():
    data = request.get_json()
    print(data)
    url=data['url']
    
    video_id=get_video_id(url)
    print(video_id)
    if not video_id:
        return jsonify({"error": "video_id parameter is required"}), 400 
    
    video_data = fetch_video_data_numbers(video_id)
    comments_data = fetch_video_comments(video_id)
  #  print(type(comments_data))
    #print(comments_data["comments"])
    
    
    
    if "error" in video_data:
       return jsonify(video_data), 500
    
    return jsonify([video_data, comments_data]), 200  
@app.route('/historical_data', methods=['POST'])
def get_historical_data():
    data = request.get_json()
    print(data)
    url=data['url']
    
    video_id=get_video_id(url)
    print(video_id)
    if not video_id:
        return jsonify({"error": "video_id parameter is required"}), 400 
    
    fetch_video_data(video_id)
    print('p')
    print(video_id)
    print('p')
    video_data = process_queue(video_id)  # Now returns the video data
    print('h')
    print(video_data)
    print('h')
    if not video_data or "error" in video_data:
        return jsonify({"error": "Failed to fetch video data"}), 500

    return jsonify(video_data), 200


if __name__ == '__main__':
    app.run(debug=True)
