import matplotlib.pyplot as plt
from utils.sentiment_analysis import analyze_sentiment

def plot_sentiment(video_id):
    
    positives,negatives,neutral,total = analyze_sentiment(video_id)['positive'],analyze_sentiment(video_id)['negative'],analyze_sentiment(video_id)['neutral'],analyze_sentiment(video_id)['total']
    if total == 0:
        print("No comments to analyze.")
    sentiment_counts = [positives, negatives, neutral]
    labels = ["Positive", "Negative", "Neutral"]
    colors = ["green","red","grey"]
    plt.figure(figsize=(6, 6))
    plt.pie(sentiment_counts, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title(f"Sentiment Analysis of Comments ({total} Comments)")
    plt.show()

if __name__ == "__main__":
    video_id = "sF5LYGgKbUA"

    print("Generating sentiment analysis visualization...")
    plot_sentiment(video_id)