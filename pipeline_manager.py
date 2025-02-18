import sys
from src.logger import get_logger
from src.exception import CustomException
from src.components.binance.data_fetcher import DataFetcher
from src.components.binance.data_preprocessor import DataPreprocessor
from src.components.twitter.data_fetcher import TwitterDataFetcher
from src.components.twitter.data_preprocessor import TextDataPreprocessor
import argparse

logger = get_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting the cryptocurrency data pipeline...")
        print("Starting the cryptocurrency data pipeline...")

        # Argument parser setup
        parser = argparse.ArgumentParser(description="Fetch cryptocurrency data from Binance and Twitter")
        parser.add_argument("--coin_name", type=str, help="Name of the cryptocurrency (e.g., ethereum, bitcoin)", required=True)
        parser.add_argument("--interval", type=str, default="1d", help="Time interval (e.g., 1m, 1h, 1d)")
        parser.add_argument("--limit", type=int, default=365, help="Number of data points to fetch")
        parser.add_argument("--twitter_query", type=str, help="Query to search for on Twitter (e.g., bitcoin)")
        parser.add_argument("--tweet_count", type=int, default=10, help="Number of tweets to fetch")

        args = parser.parse_args()

        # Step 1: Fetch data from Binance
        print("Step 1: Fetching data from Binance...")
        fetcher = DataFetcher(coin_name=args.coin_name, interval=args.interval, limit=args.limit)
        raw_data = fetcher.fetch_klines()
        print("Step 1 completed.")

        # Step 2: Preprocess the Binance data
        print("Step 2: Processing the Binance data...")
        preprocessor = DataPreprocessor()
        df = preprocessor.process_klines(raw_data)
        print("Step 2 completed.")

        # Step 3: Save Binance data to CSV
        print("Step 3: Saving Binance data to CSV...")
        preprocessor.save_to_csv(df, file_path="artifacts/crypto_data.csv")
        print("Step 3 completed.")

        # Step 4: Fetch data from Twitter
        print("Step 4: Fetching data from Twitter...")
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAAF8ywEAAAAA0hoNDdXS14SEpuArPa80kx9Dvfc%3DBgIaZ11TXR8WNObPbQmc3M0hTp9I34sc1BzN0yturEOQnzQMJJ"
        twitter_fetcher = TwitterDataFetcher(bearer_token=bearer_token)

        query = f"${args.coin_name} lang:en -is:retweet"  # Exclude retweets
        tweet_data = twitter_fetcher.fetch_tweets(query=query, max_results=args.tweet_count)
        print("Step 4 completed.")

        # Step 5: Preprocess the Twitter data
        print("Step 5: Processing the Twitter data...")
        text_preprocessor = TextDataPreprocessor()
        tweet_df = text_preprocessor.process_tweets(tweet_data)
        print("Step 5 completed.")

        # Step 6: Save Twitter data to CSV
        print("Step 6: Saving Twitter data to CSV...")
        text_preprocessor.save_to_csv(tweet_df, file_path="artifacts/twitter_data.csv")
        print("Step 6 completed.")

        # Step 7: Display first few rows of both datasets
        print("Step 7: Displaying processed data samples...")
        print("Binance Data:")
        print(df.head())
        print("Twitter Data:")
        print(tweet_df.head())

        logger.info("Pipeline executed successfully!")
        print("Pipeline executed successfully!")

    except Exception as e:
        logger.error(f"An error occurred in the pipeline: {e}")
        print(f"An error occurred in the pipeline: {e}")
        raise CustomException(e, sys)