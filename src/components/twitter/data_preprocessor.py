import pandas as pd
import os
from src.logger import get_logger

logger = get_logger()

class TextDataPreprocessor:
    @staticmethod
    def process_tweets(tweet_data):
        """Convert tweet data to a DataFrame and clean it."""
        df = pd.DataFrame(tweet_data)

        # Convert datetime to a more readable format
        df["created_at"] = pd.to_datetime(df["created_at"])

        logger.info("Tweet data successfully processed and cleaned.")
        return df

    @staticmethod
    def save_to_csv(df, file_path="artifacts/twitter_data.csv"):
        """Save the DataFrame to a CSV file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
        df.to_csv(file_path, index=False)
        logger.info(f"Tweet data successfully saved to {file_path}")