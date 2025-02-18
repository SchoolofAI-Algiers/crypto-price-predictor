import yfinance as yf
import pandas as pd
from src.logger import get_logger
from src.exception import CustomException

logger = get_logger()

class YahooFinanceFetcher:
    def __init__(self, ticker):
        """
        Initializes the fetcher with the asset's ticker (e.g., BTC-USD, ETH-USD, AAPL, etc.).
        
        Args:
            ticker (str): The asset's ticker (e.g., "BTC-USD" for Bitcoin).
        """
        self.ticker = ticker

    def fetch_historical_data(self, start, end, interval="1d"):
        """
        Fetches historical data for the specified asset between start and end dates.
        
        Args:
            start (str): Start date in the format "YYYY-MM-DD".
            end (str): End date in the format "YYYY-MM-DD".
            interval (str): Data interval (e.g., "1m", "1h", "1d", "1wk").
        
        Returns:
            pd.DataFrame: A DataFrame containing the historical data.
        """
        try:
            logger.info(f"Fetching historical data for {self.ticker} from {start} to {end}...")
            data = yf.download(
                tickers=self.ticker,
                start=start,
                end=end,
                interval=interval,
                progress=False
            )
            data.reset_index(inplace=True)  # Convertir l'index en colonne
            logger.info(f"Successfully fetched {len(data)} rows of data.")
            return data
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data: {e}")
            raise CustomException(f"Yahoo Finance API Request Failed: {e}")