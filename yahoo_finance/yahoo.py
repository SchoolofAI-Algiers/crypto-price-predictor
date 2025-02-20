import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import json
import re
import os


def get_yahoo_news(query, max_articles=100):
    """
    Fetch news articles from Yahoo Finance
    
    Parameters:
    query (str): Search term (e.g., 'AAPL', 'cryptocurrency', 'Tesla')
    max_articles (int): Maximum number of articles to fetch
    """
    
    # Base URL for Yahoo Finance news API
    base_url = "https://query2.finance.yahoo.com/v1/finance/search"
    
    news_data = []
    offset = 0
    count = 0
    
    try:
        while count < max_articles:
            # Parameters for the API request
            params = {
                'q': query,
                'quotes_count': 0,
                'news_count': 20,  # Max news per request
                'start': offset,
                'lang': 'en-US',
                'region': 'US'
            }
            
            # Make the request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(base_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'news' not in data or not data['news']:
                    break
                
                for article in data['news']:
                    try:
                        # Get article content
                        article_content = get_article_content(article['link'])
                        
                        news_item = {
                            'title': article.get('title', ''),
                            'publisher': article.get('publisher', ''),
                            'publish_date': datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                            'link': article.get('link', ''),
                            'type': article.get('type', ''),
                            'content': article_content
                        }
                        
                        news_data.append(news_item)
                        count += 1
                        
                        print(f"Fetched article {count}: {news_item['title'][:50]}...")
                        
                        if count >= max_articles:
                            break
                        
                        # Add delay to avoid rate limiting
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"Error processing article: {str(e)}")
                        continue
                
                offset += 20
                
            else:
                print(f"Error: Status code {response.status_code}")
                break
                
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
    
    return news_data

def get_article_content(url):
    """Extract article content from the URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find article content (adjust selectors based on website structure)
        content = ''
        
        # Try different common article content selectors
        content_selectors = [
            'article',
            '.article-body',
            '.article-content',
            '#article-body',
            '.content-article'
        ]
        
        for selector in content_selectors:
            article_content = soup.select_one(selector)
            if article_content:
                # Get all paragraphs
                paragraphs = article_content.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
                break
        
        return content
        
    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return ''


def save_news_data(news_data, query, start_date=None):
    """Save news data to CSV and JSON files in ./yahoo directory"""
    if not news_data:
        print("No news data to save")
        return
    
    # Create yahoo directory if it doesn't exist
    import os
    save_dir = "./yahoo_finance"
    os.makedirs(save_dir, exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame(news_data)
    
    # Generate filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create full file paths
    csv_filename = os.path.join(save_dir, f"yahoo_finance_news_{query}_{timestamp}.csv")
    json_filename = os.path.join(save_dir, f"yahoo_finance_news_{query}_{timestamp}.json")
    
    # Save to CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"Saved news data to {csv_filename}")
    
    # Save to JSON
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    print(f"Saved news data to {json_filename}")
    
    return df


def main():
    # Example searches
    searches = [
        'cryptocurrency',
        'Bitcoin',
        'Tesla',
        'AAPL',
        'artificial intelligence'
    ]
    
    for query in searches:
        print(f"\nFetching news for: {query}")
        news_data = get_yahoo_news(query, max_articles=50)
        save_news_data(news_data, query)
        # Add delay between searches
        time.sleep(2)

if __name__ == "__main__":
    main()