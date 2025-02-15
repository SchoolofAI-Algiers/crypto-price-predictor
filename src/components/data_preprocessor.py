import pandas as pd
import os
from src.logger import get_logger

logger = get_logger()

class DataPreprocessor:
    @staticmethod
    def process_klines(data):
        """Convert Binance API data to a DataFrame and clean it."""
        columns = ["Open_Time", "Open", "High", "Low", "Close", "Volume", 
                   "Close_Time", "Quote_Asset_Volume", "Number_of_Trades", 
                   "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume", "Ignore"]
        
        df = pd.DataFrame(data, columns=columns)

        # Convert timestamps to datetime
        df["Open_Time"] = pd.to_datetime(df["Open_Time"], unit="ms")
        df["Close_Time"] = pd.to_datetime(df["Close_Time"], unit="ms")

        # Convert numerical values to float
        num_cols = ["Open", "High", "Low", "Close", "Volume", 
                    "Quote_Asset_Volume", "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume"]
        
        df[num_cols] = df[num_cols].astype(float)

        logger.info("Data successfully processed and cleaned.")
        return df

    @staticmethod
    def save_to_csv(df, file_path="artifacts/crypto_data.csv"):
        """Save the DataFrame to a CSV file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
        df.to_csv(file_path, index=False)
        logger.info(f"Data successfully saved to {file_path}")
