# pipeline_manager.py - Main execution script
import sys
from src.logger import get_logger
from src.exception import CustomException
from src.components.data_fetcher import DataFetcher
from src.components.data_preprocessor import DataPreprocessor
import argparse

logger = get_logger()

if __name__ == "__main__": 
    try:
        logger.info("Starting the Reddit Sentiment Analysis pipeline...")
        print("Starting the Reddit Sentiment Analysis pipeline...")

        # Step 1: Fetch data from Reddit
        print("Step 1: Fetching data from Reddit...")
        parser = argparse.ArgumentParser(description="Fetch Reddit data")
        parser.add_argument("--start_date", type=str, required=True, help="Start date (YYYY-MM-DD)")
        parser.add_argument("--end_date", type=str, required=True, help="End date (YYYY-MM-DD)")
        parser.add_argument("--interval", type=str, choices=["hour", "day"], default="hour", help="Time interval")
        parser.add_argument("--limit", type=int, default=500, help="Maximum number of posts to fetch per subreddit")
        parser.add_argument("--crypto", type=str, default="BTC", help="Cryptocurrency to analyze (e.g., BTC, ETH, SOL)")
        args = parser.parse_args()

        fetcher = DataFetcher(crypto=args.crypto)
        raw_data = fetcher.fetch_reddit_posts(args.start_date, args.end_date, args.limit)
        print("Step 1 completed.")

        # Step 2: Process sentiment data
        print("Step 2: Processing the data...")
        preprocessor = DataPreprocessor()
        sentiment_data = preprocessor.process_sentiment_data(raw_data, args.start_date, args.end_date, args.interval)
        print("Step 2 completed.")

        # Step 3: Save results
        print("Step 3: Saving data...")
        preprocessor.save_to_csv(raw_data, "artifacts/reddit_raw.csv")
        preprocessor.save_to_csv(sentiment_data, "artifacts/reddit_sentiment.csv")
        print("Step 3 completed.")

        print("Pipeline executed successfully!")
        logger.info("Pipeline executed successfully!")

    except Exception as e:
        logger.error(f"An error occurred in the pipeline: {e}")
        print(f"An error occurred in the pipeline: {e}")
        raise CustomException(e, sys)
