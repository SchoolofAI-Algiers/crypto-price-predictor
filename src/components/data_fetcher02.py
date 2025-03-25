import requests
import pandas as pd
import time
import datetime
from src.logger import get_logger
from src.exception import CustomException

logger = get_logger()

# Cryptocurrency symbol mapping
symbol_map = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "binance-coin": "BNBUSDT",
    "ripple": "XRPUSDT",
    "cardano": "ADAUSDT",
    "solana": "SOLUSDT",
    "polkadot": "DOTUSDT",
    "dogecoin": "DOGEUSDT",
    "shiba-inu": "SHIBUSDT",
    "litecoin": "LTCUSDT",
    "chainlink": "LINKUSDT",
    "polygon": "MATICUSDT",
    "avalanche": "AVAXUSDT",
    "uniswap": "UNIUSDT",
    "cosmos": "ATOMUSDT",
    "stellar": "XLMUSDT",
    "vechain": "VETUSDT",
    "filecoin": "FILUSDT",
    "algorand": "ALGOUSDT",
    "monero": "XMRUSDT",
    "bitcoin-cash": "BCHUSDT",
    "eos": "EOSUSDT",
    "tezos": "XTZUSDT",
    "aave": "AAVEUSDT",
    "compound": "COMPUSDT",
    "maker": "MKRUSDT",
}

class DataFetcher:
    def __init__(self, coin_name="ethereum", interval="1d", start_date="2024-01-01"):
        self.coin = coin_name
        self.interval = interval
        self.start_date = start_date
        self.url = "https://api.binance.com/api/v3/klines"

    def fetch_klines(self):
        """Fetch all historical data from Binance API starting from the given date"""
        all_data = []
        start_timestamp = int(datetime.datetime.strptime(self.start_date, "%Y-%m-%d").timestamp() * 1000)
        end_time = None  # Fetch the most recent data first

        while True:
            params = {
                "symbol": symbol_map[self.coin],
                "interval": self.interval,
                "limit": 1000,  # Fetch max 1000 rows per request
            }
            if end_time:
                params["endTime"] = end_time  # Fetch older data

            try:
                response = requests.get(self.url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data or data[-1][0] < start_timestamp:
                    break  # Stop when reaching the start date

                all_data.extend(data)
                end_time = data[0][0] - 1  # Move the window back for older data
                time.sleep(1)  # Respect Binance API rate limits

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching Binance data: {e}")
                raise CustomException(f"API Request Failed: {e}")

        # Filter data that is older than the start date
        all_data = [row for row in all_data if row[0] >= start_timestamp]

        return all_data
