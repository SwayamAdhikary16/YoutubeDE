import os 
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from historical_data import get_historical_data
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.sentiment_analysis import analyze_sentiment
from utils import youtube_api as yt

def plot_time_series(video_id):
    """
    Plots time series data for views and likes from historical data.
    """
    historical_data = get_historical_data(video_id)

    if not historical_data["timestamps"]:
        print("No historical data available for plotting.")
        return

    # Convert timestamps to datetime objects
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in historical_data["timestamps"]]
    views = list(map(int, historical_data["views"]))
    likes = list(map(int, historical_data["likes"]))
    comments = list(map(int, historical_data["comments"]))

    plt.figure(figsize=(10, 5))
    
    # Plot Views
    plt.plot(timestamps, views, label="Views", marker="o", linestyle="-", color="blue")
    
    # Plot Likes
    plt.plot(timestamps, likes, label="Likes", marker="s", linestyle="--", color="green")
    
    # Plot Comments
    plt.plot(timestamps, comments, label="Comments", marker="x", linestyle="-.", color="red")
    # Formatting the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))  # Adjust intervals as needed
    plt.xticks(rotation=45)
    
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.title("YouTube Video Views & Likes Over Time")
    plt.legend()
    plt.grid()
    plt.show()


def plot_sentiment(video_id):
    """
    Plots a pie chart for sentiment analysis based on comments.
    """
    sentiment_result = analyze_sentiment(video_id)
    
    positives, negatives, neutral, total = (
        sentiment_result["positive"],
        sentiment_result["negative"],
        sentiment_result["neutral"],
        sentiment_result["total"],
    )

    if total == 0:
        print("No comments to analyze.")
        return

    sentiment_counts = [positives, negatives, neutral]
    labels = ["Positive", "Negative", "Neutral"]
    colors = ["green", "red", "grey"]

    plt.figure(figsize=(6, 6))
    plt.pie(sentiment_counts, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title(f"Sentiment Analysis of Comments ({total} Comments)")
    plt.show()


if __name__ == "__main__":
    video_id = "sF5LYGgKbUA"

    print("Generating time-series visualization...")
    plot_time_series(video_id)

    # print("Generating sentiment analysis visualization...")
    # plot_sentiment(video_id)
