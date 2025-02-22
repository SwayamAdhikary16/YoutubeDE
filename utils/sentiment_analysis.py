import sys
import os 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import utils.youtube_api as yt 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(video_id):
    """
    Analyzes the sentiment of comments on a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        dict: A dictionary containing the count of positive, negative, and neutral comments, 
              as well as the total number of comments analyzed.
              {
                  "positive": int,
                  "negative": int,
                  "neutral": int,
                  "total": int
                }
    """
    # function input output
    # Initialize counters for sentiment categories
    positives = 0 
    negatives = 0
    neutral = 0 

    # Fetch comments for the given video ID
    comms = yt.fetch_video_comments(video_id)
    comments = comms["comments"]
    # Analyze each comment's sentiment
    for comment in comments:
        sentiment_scores = analyzer.polarity_scores(comment)
        compound_score = sentiment_scores["compound"]

        # Categorize the comment based on the compound score
        if compound_score >= 0.05:
            positives += 1
        elif compound_score <= -0.05:
            negatives += 1
        else:
            neutral += 1

    # Return the sentiment analysis results
    return {
        "positive": positives,
        "negative": negatives,
        "neutral": neutral,
        "total": len(comments)
    }
