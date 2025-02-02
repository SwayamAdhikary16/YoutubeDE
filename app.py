from flask import Flask, jsonify, request
import requests
from utils.youtube_api import fetch_video_data_numbers, fetch_video_comments, get_video_id
from components.historical_data import fetch_video_data, process_queue

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/fetch_video_data', methods=['POST'])
def api_fetch_video_data():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "url parameter is required"}), 400
    
    video_id = get_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid video URL"}), 400
    
    video_data = fetch_video_data_numbers(video_id)
    comments_data = fetch_video_comments(video_id)
    
    if "error" in video_data:
        return jsonify(video_data), 500
    
    return jsonify([video_data, comments_data]), 200

@app.route('/historical_data', methods=['POST'])
def get_historical_data():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "url parameter is required"}), 400
    
    video_id = get_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid video URL"}), 400
    
    fetch_video_data(video_id)
    video_data = process_queue(video_id)
    
    if not video_data or "error" in video_data:
        return jsonify({"error": "Failed to fetch video data"}), 500
    
    return jsonify(video_data), 200

if __name__ == '__main__':
    app.run(debug=True)
