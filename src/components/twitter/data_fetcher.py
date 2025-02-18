import tweepy
import pandas as pd
from src.logger import get_logger
from src.exception import CustomException

logger = get_logger()

class TwitterDataFetcher:
    def __init__(self, bearer_token):
        """Initialize the Twitter API client with a bearer token."""
        self.client = tweepy.Client(bearer_token=bearer_token)

    def fetch_tweets(self, query, max_results=10):
        """
        Fetch tweets based on a query using Twitter API v2.
        
        Args:
            query (str): The search query for tweets.
            max_results (int): Maximum number of tweets to fetch.
        
        Returns:
            list: A list of dictionaries containing tweet data.
        """
        try:
            # Fetch tweets using the search_recent_tweets method
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics"]
            )

            # Extract relevant tweet data
            tweet_data = []
            if tweets.data:
                for tweet in tweets.data:
                    tweet_data.append({
                        "id": tweet.id,
                        "created_at": tweet.created_at,
                        "text": tweet.text,
                        "retweet_count": tweet.public_metrics["retweet_count"],
                        "like_count": tweet.public_metrics["like_count"],
                        "reply_count": tweet.public_metrics["reply_count"],
                        "quote_count": tweet.public_metrics["quote_count"]
                    })

            logger.info(f"Successfully fetched {len(tweet_data)} tweets.")
            return tweet_data

        except Exception as e:
            logger.error(f"Error fetching Twitter data: {e}")
            raise CustomException(f"Twitter API Request Failed: {e}")