import pandas as pd
from datetime import datetime
import logging.config
from typing import Optional
import os
from ..scraper.crypto_scraper import CryptoContentScraper
from ..config.config import ARTIFACTS_DIR, LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class PipelineManager:
    def __init__(self):
        self.scraper = CryptoContentScraper()

    def run_pipeline(self, start_date: datetime, end_date: datetime, num_pages: int = 3) -> Optional[pd.DataFrame]:
        """
        Run the data collection pipeline
        
        Args:
            start_date (datetime): Start date for news collection
            end_date (datetime): End date for news collection
            num_pages (int): Number of pages to scrape
            
        Returns:
            Optional[pd.DataFrame]: Collected data as DataFrame
        """
        logger.info(f"Starting pipeline run from {start_date} to {end_date}")

        try:
            # Collect news data
            news_data = self.scraper.get_crypto_news(start_date, end_date, num_pages)

            if not news_data:
                logger.warning("No data was collected!")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(news_data)
            
            # Save to CSV
            self._save_data(df)

            return df

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return None

    def _save_data(self, df: pd.DataFrame) -> None:
        """Save data to CSV file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(ARTIFACTS_DIR, f'crypto_content_{timestamp}.csv')
        
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
        logger.info(f"Total items collected: {len(df)}")
        logger.info(f"Content breakdown:\n{df['content_type'].value_counts()}")