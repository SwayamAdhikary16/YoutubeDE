import youtube_api as yt 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import googleapiclient.discovery

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(video_id):
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