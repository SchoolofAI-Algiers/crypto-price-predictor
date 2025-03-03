import sys
from src.logger import get_logger
from src.exception import CustomException
from src.components.data_fetcher import DataFetcher
from src.components.data_preprocessor import DataPreprocessor
import argparse
from src.components.model import Model
from src.components.data_loader import load_and_preprocess_data

logger = get_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting the cryptocurrency data pipeline...")
        print("Starting the cryptocurrency data pipeline...")

        # Step 1: Fetch data from Binance
        # print("Step 1: Fetching data from Binance...")
        # # Argument parser setup
        # parser = argparse.ArgumentParser(description="Fetch cryptocurrency data from Binance")
        # parser.add_argument("--coin_name", type=str, help="Name of the cryptocurrency (e.g., ethereum, bitcoin)", required=True)
        # parser.add_argument("--interval", type=str, default="1d", help="Time interval (e.g., 1m, 1h, 1d)")
        # parser.add_argument("--limit", type=int, default=365, help="Number of data points to fetch")

        # args = parser.parse_args()
        # # Use arguments to fetch data
        # fetcher = DataFetcher(coin_name=args.coin_name, interval=args.interval, limit=args.limit)
        # raw_data = fetcher.fetch_klines()

        # print("Step 1 completed.")

        # # Step 2: Preprocess the data
        # print("Step 2: Processing the data...")
        # preprocessor = DataPreprocessor()
        # df = preprocessor.process_klines(raw_data)
        # print("Step 2 completed.")

        # # Step 3: Save to CSV
        # print("Step 3: Saving data to CSV...")
        # preprocessor.save_to_csv(df, file_path="artifacts/crypto_data.csv")
        # print("Step 3 completed.")

        # # Step 4: Display first few rows
        # print("Step 4: Displaying processed data sample...")
        # print(df.head())
        print("Step 5: Load data")
        filepath = 'artifacts/crypto_data.csv'  # Replace with your CSV file path
        X_train, X_test, y_train, y_test,scaler= load_and_preprocess_data(filepath)
        print("Step 6: Train the model")
        print(X_train.shape)
        print(y_train.shape)
        print(X_test.shape)
        print(y_test.shape)

        model=Model(128,50)
        model.define_model()
        history=model.train(X_train,y_train)
        model.evaluation(history,X_test,y_test,scaler)

        logger.info("Pipeline executed successfully!")
        print("Pipeline executed successfully!")

    except Exception as e:
        logger.error(f"An error occurred in the pipeline: {e}")
        print(f"An error occurred in the pipeline: {e}")
        raise CustomException(e, sys)
