import praw
import pandas as pd
import datetime
from datetime import timezone
import nest_asyncio
import time
import os
nest_asyncio.apply()

def convert_timestamp_to_date(timestamp):
    """Convert Unix timestamp to readable date format"""
    return datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def get_reddit_data(start_date, end_date, limit=100):
    """
    Fetch Reddit data within specified date range
    
    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    limit (int): Maximum number of posts to fetch
    """
    # Convert date strings to datetime objects
    start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc) + datetime.timedelta(days=1)
    
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id="xuyvILjULWhYVTdTyzZtVA",
        client_secret="8VpNCxviBRy81ylWF7SMzV2a9Iklhg",
        user_agent="script:crypto_data_collector:v1.0 (by /u/YourUsername)"
    )
    
    # Initialize data list
    data = []
    
    try:
        subreddit = reddit.subreddit("cryptocurrency")
        
        # Fetch posts from different sorting methods to increase coverage
        for sorting_method in ['hot', 'new', 'top']:
            print(f"Fetching {sorting_method} posts...")
            
            if sorting_method == 'top':
                posts = subreddit.top(time_filter='month', limit=limit)
            elif sorting_method == 'hot':
                posts = subreddit.hot(limit=limit)
            else:
                posts = subreddit.new(limit=limit)
            
            for post in posts:
                post_date = datetime.datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                
                # Check if post is within date range
                if start_datetime <= post_date <= end_datetime:
                    print(f"Found post from {post_date}")
                    
                    try:
                        # Get comments with error handling
                        post.comments.replace_more(limit=0)
                        
                        # Basic post data without comments
                        post_data = {
                            "post_title": post.title,
                            "post_score": post.score,
                            "post_url": post.url,
                            "post_date": convert_timestamp_to_date(post.created_utc),
                            "comment": "",
                            "comment_date": "",
                            "comment_score": ""
                        }
                        
                        # Add entry with just post data (no comment)
                        data.append(post_data.copy())
                        
                        # Add entries for each comment
                        for comment in post.comments.list():
                            new_entry = post_data.copy()
                            new_entry["comment"] = comment.body
                            new_entry["comment_date"] = convert_timestamp_to_date(comment.created_utc)
                            new_entry["comment_score"] = comment.score
                            data.append(new_entry)
                            
                        # Add small delay to avoid rate limiting
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f"Error processing post {post.id}: {str(e)}")
                        continue
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        if len(df) > 0:
            # Save to CSV
            output_dir = "./reddit"
            os.makedirs(output_dir, exist_ok=True)
            # Save to CSV inside the 'reddit' directory
            filename = os.path.join(output_dir, f"reddit_crypto_data_{start_date}_to_{end_date}.csv")
            #filename = f"reddit_crypto_data_{start_date}_to_{end_date}.csv"
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
            print(f"Collected {len(df)} entries")
        else:
            print("No data found in the specified date range")
            
        return df
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Get current date and 7 days ago
    end_date = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d')
    start_date = (datetime.datetime.now(timezone.utc) - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    
    print(f"Fetching data from {start_date} to {end_date}")
    df = get_reddit_data(start_date, end_date, limit=100)
    
    if df is not None:
        print(f"Data collection completed")

if __name__ == "__main__":
    main()