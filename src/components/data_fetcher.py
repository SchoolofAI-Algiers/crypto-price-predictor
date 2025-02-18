import praw
import pandas as pd
import time
from src.logger import get_logger
from src.exception import CustomException
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

logger = get_logger()

class DataFetcher:
    CRYPTO_CONFIG = {
        'BTC': {
            'keywords': ['bitcoin', 'btc', 'satoshi', 'bitcoin price', 'bitcoin halving'],
            'subreddits': ['Bitcoin', 'CryptoCurrency', 'CryptoMarkets', 'btc']
        },
        'ETH': {
            'keywords': ['ethereum', 'eth', 'vitalik', 'ethereum price', 'eth2'],
            'subreddits': ['ethereum', 'CryptoCurrency', 'CryptoMarkets', 'ethtrader']
        },
        'SOL': {
            'keywords': ['solana', 'sol', 'solana price'],
            'subreddits': ['solana', 'CryptoCurrency', 'CryptoMarkets']
        },
        'DOGE': {
            'keywords': ['dogecoin', 'doge', 'doge price'],
            'subreddits': ['dogecoin', 'CryptoCurrency', 'CryptoMarkets']
        },
    }

    def __init__(self, crypto='BTC'):
        # Validate environment variables
        required_env_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        if crypto not in self.CRYPTO_CONFIG:
            raise ValueError(f"Unsupported cryptocurrency: {crypto}")
        
        self.crypto = crypto
        self.subreddits = self.CRYPTO_CONFIG[crypto]['subreddits']
        self.keywords = self.CRYPTO_CONFIG[crypto]['keywords']
        logger.info(f"Initialized DataFetcher for {crypto}")
        logger.info(f"Using subreddits: {self.subreddits}")
        logger.info(f"Using keywords: {self.keywords}")

    def is_crypto_related(self, title, text):
        title = str(title).lower()
        text = str(text).lower()
        combined_text = title + " " + text
        for keyword in self.keywords:
            if keyword in combined_text:
                return True
        return False

    def fetch_reddit_posts(self, start_date, end_date, limit=500):
        start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()) + 86400
        
        logger.info(f"Fetching posts between {start_date} and {end_date}")
        logger.info(f"Timestamps: {start_timestamp} to {end_timestamp}")

        data = []
        total_posts_seen = 0
        
        for subreddit_name in self.subreddits:
            try:
                logger.info(f"Fetching from r/{subreddit_name}")
                subreddit = self.reddit.subreddit(subreddit_name)
                posts = subreddit.new(limit=limit)
                
                subreddit_posts = 0
                for post in posts:
                    total_posts_seen += 1
                    post_time = post.created_utc
                    
                    if start_timestamp <= post_time < end_timestamp and self.is_crypto_related(post.title, post.selftext):
                        data.append({
                            "subreddit": subreddit_name,
                            "title": post.title,
                            "text": post.selftext,
                            "upvotes": post.score,
                            "num_comments": post.num_comments,
                            "created_utc": post_time,
                            "cryptocurrency": self.crypto  # Add crypto identifier to the data
                        })
                        subreddit_posts += 1
                
                logger.info(f"Found {subreddit_posts} matching posts in r/{subreddit_name}")
                
            except Exception as e:
                logger.error(f"Error fetching from r/{subreddit_name}: {str(e)}")
                continue

        logger.info(f"Total posts processed: {total_posts_seen}")
        logger.info(f"Total matching posts: {len(data)}")
        
        df = pd.DataFrame(data)
        if df.empty:
            logger.warning("No posts were found matching the criteria!")
        return df
