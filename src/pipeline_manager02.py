import sys
import os
import argparse
import pandas as pd
from src.logger import get_logger
from src.exception import CustomException
from src.components.data_fetcher import DataFetcher
from src.components.data_preprocessor import DataPreprocessor

logger = get_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting the cryptocurrency data pipeline...")
        print("Starting the cryptocurrency data pipeline...")

        # Step 1: Fetch data from Binance
        print("Step 1: Fetching data from Binance...")

        # Argument parser setup
        parser = argparse.ArgumentParser(description="Fetch cryptocurrency data from Binance")
        parser.add_argument("--coin_name", type=str, help="Name of the cryptocurrency (e.g., ethereum, bitcoin)", required=True)
        parser.add_argument("--interval", type=str, default="1d", help="Time interval (e.g., 1m, 1h, 1d)")
        parser.add_argument("--start_date", type=str, required=True, help="Start date in YYYY-MM-DD format")
        
        args = parser.parse_args()

        # Fetch data
        fetcher = DataFetcher(coin_name=args.coin_name, interval=args.interval, start_date=args.start_date)
        raw_data = fetcher.fetch_klines()
        
        # Debugging: Check raw data format
        print("Raw data type:", type(raw_data))
        print("Raw data length:", len(raw_data))
        if len(raw_data) > 0:
            print("First entry sample:", raw_data[0])
        else:
            raise ValueError("No data retrieved from Binance. Check API response.")

        print("Step 1 completed.")

        # Step 2: Preprocess the data
        print("Step 2: Processing the data...")
        preprocessor = DataPreprocessor()
        df = preprocessor.process_klines(raw_data)
        
        # Debugging: Check processed data
        print("Processed data sample:")
        print(df.head())

        print("Step 2 completed.")

        # Step 3: Save to CSV
        print("Step 3: Saving data to CSV...")
        output_path = "artifacts/crypto_data.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists
        preprocessor.save_to_csv(df, file_path=output_path)
        print(f"Data successfully saved to {output_path}")

        print("Step 3 completed.")

        logger.info("Pipeline executed successfully!")
        print("Pipeline executed successfully!")

    except Exception as e:
        logger.error(f"An error occurred in the pipeline: {e}")
        print(f"An error occurred in the pipeline: {e}")
        raise CustomException(e, sys)
