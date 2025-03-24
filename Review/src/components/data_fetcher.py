import requests
import pandas as pd
import time
from src.logger import get_logger
from src.exception import CustomException

logger = get_logger()


# Human-readable cryptocurrency symbol mapping
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
    def __init__(self, coin_name="ethereum", interval="1d", limit=365):
        self.coin = coin_name
        self.interval = interval
        self.limit = limit
        self.url = "https://api.binance.com/api/v3/klines"

    def fetch_klines(self):
        """Fetch data from Binance API with pagination to get more than 1000 rows"""
        all_data = []
        end_time = None  # Start from the most recent data

        while len(all_data) < self.limit:
            params = {
                "symbol": symbol_map[self.coin],
                "interval": self.interval,
                "limit": min(self.limit - len(all_data), 1000),  # Request up to 1000 rows per API call
            }
            if end_time:
                params["endTime"] = end_time  # Set endTime to get older data

            try:
                response = requests.get(self.url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    break  # Stop if no more data is returned

                all_data.extend(data)
                end_time = data[0][0] - 1  # Update endTime to fetch older data

                time.sleep(1)  # Binance API rate limiting

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching Binance data: {e}")
                raise CustomException(f"API Request Failed: {e}")

        return all_data[:self.limit]  # Ensure we return exactly `limit` rows

