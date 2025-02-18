import pandas as pd
import os
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from src.logger import get_logger

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
logger = get_logger()

class DataPreprocessor:
    @staticmethod
    def clean_text(text):
        text = text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", '', text)
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def get_sentiment(text):
        if not text:
            return 0
        vader_score = sia.polarity_scores(text)["compound"]
        blob_score = TextBlob(text).sentiment.polarity
        return (vader_score + blob_score) / 2

    def process_sentiment_data(self, df, start_date, end_date, interval="hour"):
        if df.empty:
            logger.warning("Empty DataFrame received")
            return pd.DataFrame()

        logger.info(f"Processing DataFrame with columns: {df.columns.tolist()}")
        
        # Ensure required columns exist
        required_columns = ['title', 'text', 'created_utc']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Handle potential NaN values
        df['title'] = df['title'].fillna('')
        df['text'] = df['text'].fillna('')
        
        df["cleaned_text"] = df["title"] + " " + df["text"]
        df["cleaned_text"] = df["cleaned_text"].apply(self.clean_text)
        df["sentiment_score"] = df["cleaned_text"].apply(self.get_sentiment)
        df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")

        if interval == "hour":
            df["Timestamp"] = df["created_utc"].dt.strftime('%Y-%m-%d %H:00')
        else:
            df["Timestamp"] = df["created_utc"].dt.strftime('%Y-%m-%d')

        grouped_df = df.groupby("Timestamp").agg(
            Total_Posts=("sentiment_score", "count"),
            Avg_Sentiment=("sentiment_score", "mean"),
            Max_Sentiment=("sentiment_score", "max"),
            Min_Sentiment=("sentiment_score", "min"),
            Sentiment_Volatility=("sentiment_score", lambda x: x.max() - x.min()),
            Total_Upvotes=("upvotes", "sum"),
            Total_Comments=("num_comments", "sum"),
            Avg_Upvotes=("upvotes", "mean"),
            Avg_Comments=("num_comments", "mean"),
            Positive_Sentiment_Sum=("sentiment_score", lambda x: x[x > 0].sum()),
            Negative_Sentiment_Sum=("sentiment_score", lambda x: x[x < 0].sum()),
        ).reset_index()

        return grouped_df

    @staticmethod
    def save_to_csv(df, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.info(f"Data saved to {file_path}")
