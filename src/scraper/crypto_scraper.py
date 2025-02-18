import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from typing import List, Dict, Optional
from ..config.config import HEADERS, BASE_URL

logger = logging.getLogger(__name__)

class CryptoContentScraper:
    def __init__(self):
        self.headers = HEADERS
        self.base_url = BASE_URL

    def get_crypto_news(self, start_date: datetime, end_date: datetime, num_pages: int = 3) -> List[Dict]:
        """
        Scrape cryptocurrency news from Yahoo Finance within a date range
        
        Args:
            start_date (datetime): Start date for news collection
            end_date (datetime): End date for news collection
            num_pages (int): Number of pages to scrape
            
        Returns:
            List[Dict]: List of news articles
        """
        news_data = []
        logger.info(f"Starting news collection from {start_date} to {end_date}")

        try:
            # First try the cryptocurrency news section
            url = f"{self.base_url}/cryptocurrencies"
            logger.info(f"Fetching main crypto page: {url}")

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            main_page_articles = self._parse_main_page(soup)
            logger.info(f"Found {len(main_page_articles)} articles on main page")
            news_data.extend(main_page_articles)
            
            # Try alternative news section
            news_page_articles = self._parse_news_pages(num_pages)
            logger.info(f"Found {len(news_page_articles)} articles on news pages")
            news_data.extend(news_page_articles)

            # Filter by date range after collecting all articles
            filtered_data = self._filter_by_date_range(news_data, start_date, end_date)
            logger.info(f"Filtered to {len(filtered_data)} articles within date range")

            return filtered_data

        except Exception as e:
            logger.error(f"Error in news collection: {str(e)}")
            return []

    def _parse_main_page(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse the main cryptocurrency page"""
        news_data = []
        articles = soup.find_all('h3', {'class': 'Mb(5px)'})

        for article in articles:
            try:
                entry = self._parse_article(article)
                if entry:
                    news_data.append(entry)
            except Exception as e:
                logger.error(f"Error parsing main page article: {str(e)}")

        return news_data

    def _parse_news_pages(self, num_pages: int) -> List[Dict]:
        """Parse the news pages"""
        news_data = []

        for page in range(num_pages):
            try:
                url = f"{self.base_url}/news/crypto"
                offset = page * 20
                logger.info(f"Fetching page {page + 1}/{num_pages}: {url}" + (f"?offset={offset}" if offset > 0 else ""))

                params = {'offset': offset} if page > 0 else {}
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('div', {'class': 'Pos(r)'})
                
                page_articles = []
                for article in articles:
                    entry = self._parse_article(article, is_news_page=True)
                    if entry:
                        page_articles.append(entry)
                
                logger.info(f"Found {len(page_articles)} articles on page {page + 1}")
                news_data.extend(page_articles)

                time.sleep(2)  # Respect rate limiting

            except Exception as e:
                logger.error(f"Error in news page {page + 1}: {str(e)}")

        return news_data



    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parse article timestamp into datetime object
        Now handles more formats and special cases
        """
        if not timestamp_str:
            return None
            
        timestamp_str = timestamp_str.lower().strip()
        now = datetime.now()
        
        try:
            # Handle special cases
            if timestamp_str in ['streaming now', 'live', 'now']:
                return now
                
            # Extract numbers and time units
            numbers = ''.join(filter(str.isdigit, timestamp_str))
            
            if not numbers:
                # If no numbers found, handle special text cases
                if 'yesterday' in timestamp_str:
                    return now - timedelta(days=1)
                elif any(word in timestamp_str for word in ['just now', 'moments ago']):
                    return now
                else:
                    logger.debug(f"Unrecognized timestamp format: {timestamp_str}")
                    return now  # Default to current time if format unknown
            
            # Parse time periods
            number = int(numbers)
            if any(unit in timestamp_str for unit in ['minute', 'min', 'minutes', 'mins']):
                return now - timedelta(minutes=number)
            elif any(unit in timestamp_str for unit in ['hour', 'hr', 'hours', 'hrs']):
                return now - timedelta(hours=number)
            elif any(unit in timestamp_str for unit in ['day', 'days']):
                return now - timedelta(days=number)
            elif any(unit in timestamp_str for unit in ['week', 'weeks', 'wk', 'wks']):
                return now - timedelta(weeks=number)
            elif any(unit in timestamp_str for unit in ['month', 'months']):
                return now - timedelta(days=number * 30)
            else:
                logger.debug(f"Unrecognized time unit in: {timestamp_str}")
                return now
                
        except Exception as e:
            logger.debug(f"Error parsing timestamp {timestamp_str}: {str(e)}")
            return now  # Default to current time on error
        
    def _filter_by_date_range(self, articles: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Filter articles by date range
        More lenient filtering to avoid losing articles
        """
        filtered_articles = []
        
        for article in articles:
            timestamp_str = article.get('timestamp', '')
            
            try:
                article_date = self._parse_timestamp(timestamp_str)
                
                # If we couldn't parse the date or it's recent, include it
                if not article_date or (start_date <= article_date <= end_date):
                    # Add the parsed date to the article data
                    article['parsed_date'] = article_date.isoformat() if article_date else None
                    filtered_articles.append(article)
                    
            except Exception as e:
                logger.debug(f"Error filtering article date {timestamp_str}: {str(e)}")
                # Include articles where we couldn't parse the date
                article['parsed_date'] = None
                filtered_articles.append(article)
                
        return filtered_articles

    def _parse_article(self, article, is_news_page: bool = False) -> Optional[Dict]:
        """Parse a single article with improved timestamp handling"""
        entry = {
            'title': '',
            'source': '',
            'timestamp': '',
            'content': '',
            'link': '',
            'content_type': 'news',
            'scraped_at': datetime.now().isoformat()
        }

        try:
            if is_news_page:
                title_elem = article.find('h3')
                if title_elem:
                    entry['title'] = title_elem.text.strip()
                    link_elem = title_elem.find('a')
                    if link_elem:
                        entry['link'] = self.base_url + link_elem.get('href', '')
                
                # Try multiple ways to find the timestamp
                time_elem = (
                    article.find('span', string=lambda x: x and any(word in x.lower() 
                        for word in ['ago', 'min', 'hour', 'day', 'now', 'live'])) or
                    article.find('span', {'class': 'C(#959595)'}) or
                    article.find('time')
                )
                if time_elem:
                    entry['timestamp'] = time_elem.text.strip()
            else:
                link_elem = article.find('a')
                if link_elem:
                    entry['title'] = link_elem.text.strip()
                    entry['link'] = self.base_url + link_elem.get('href', '')

                article_container = article.find_parent('div')
                if article_container:
                    meta = article_container.find('div', {'class': 'C(#959595)'})
                    if meta:
                        source_parts = meta.text.split('·')
                        entry['source'] = source_parts[0].strip() if source_parts else ''
                        if len(source_parts) > 1:
                            entry['timestamp'] = source_parts[1].strip()

            content = article.find('p')
            if content:
                entry['content'] = content.text.strip()

            # Only return if we have at least a title or content
            if entry['title'] or entry['content']:
                return entry
            return None

        except Exception as e:
            logger.error(f"Error parsing article content: {str(e)}")
            return None