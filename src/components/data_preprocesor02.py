import pandas as pd
import os
from src.logger import get_logger
from sklearn.preprocessing import MinMaxScaler

logger = get_logger()

class DataPreprocessor:
    def __init__(self, resample_interval=None, normalize=False):
        """
        Initialize the DataPreprocessor.

        :param resample_interval: Time interval for resampling (e.g., '1H' for hourly).
        :param normalize: Whether to apply MinMax normalization.
        """
        self.resample_interval = resample_interval
        self.normalize = normalize
        self.scaler = MinMaxScaler() if normalize else None

    def process_klines(self, data):
        """Convert Binance API data to a cleaned DataFrame for time series modeling."""
        columns = ["Open_Time", "Open", "High", "Low", "Close", "Volume", 
                   "Close_Time", "Quote_Asset_Volume", "Number_of_Trades", 
                   "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume", "Ignore"]
        
        df = pd.DataFrame(data, columns=columns)

        # Convert timestamps to datetime
        df["Open_Time"] = pd.to_datetime(df["Open_Time"], unit="ms")

        # Drop unnecessary columns
        df.drop(columns=["Close_Time", "Ignore"], inplace=True)

        # Convert numerical values to float
        num_cols = ["Open", "High", "Low", "Close", "Volume", 
                    "Quote_Asset_Volume", "Taker_Buy_Base_Volume", "Taker_Buy_Quote_Volume"]
        
        df[num_cols] = df[num_cols].astype(float)

        # Set Open_Time as the index
        df.set_index("Open_Time", inplace=True)

        # Sort data by time
        df.sort_index(inplace=True)

        # Handle missing values
        df.fillna(method="ffill", inplace=True)  # Forward-fill missing values
        df.fillna(method="bfill", inplace=True)  # Backward-fill if needed

        # Feature Engineering
        if len(df) > 1:  # Ensure there is enough data
            df["Return"] = df["Close"].pct_change().fillna(0)  # Fill first NaN with 0
            df["Volatility"] = df["Return"].rolling(window=5, min_periods=1).std().fillna(0)
            df["MA_Close"] = df["Close"].rolling(window=5, min_periods=1).mean().fillna(df["Close"])
        else:
            df["Return"] = 0
            df["Volatility"] = 0
            df["MA_Close"] = df["Close"]

        # Resampling (if needed)
        if self.resample_interval:
            df = df.resample(self.resample_interval).agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
                "Quote_Asset_Volume": "sum",
                "Taker_Buy_Base_Volume": "sum",
                "Taker_Buy_Quote_Volume": "sum",
                "Number_of_Trades": "sum",
                "Return": "sum",
                "Volatility": "mean",
                "MA_Close": "mean"
            }).dropna(how="all")  # Remove empty rows after resampling

        # Apply Normalization if enabled
        if self.normalize and not df.empty:
            df[num_cols] = self.scaler.fit_transform(df[num_cols])

        logger.info("Data successfully processed and cleaned.")
        return df

    def save_to_csv(self, df, file_path="artifacts/crypto_data.csv"):
        """Save the DataFrame to a CSV file."""
        if df.empty:
            logger.warning("DataFrame is empty. Skipping CSV save.")
            return
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
        df.to_csv(file_path, index=True)
        logger.info(f"Data successfully saved to {file_path}")
