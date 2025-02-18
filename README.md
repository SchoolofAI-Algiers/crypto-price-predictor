# Crypto Price Predictor

A Deep Learning-Based Cryptocurrency Price Prediction System that analyzes Reddit sentiment data for various cryptocurrencies.

## Project Description

This project collects and analyzes Reddit posts related to different cryptocurrencies to gauge market sentiment. It processes posts from various cryptocurrency-related subreddits and performs sentiment analysis on the collected data.

## Setup

1. Clone the repository:

```bash
git clone [repository-url]
cd crypto-price-predictor
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root with your Reddit API credentials:

```ini
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## Usage

The pipeline can be run using the following command line arguments:

```bash
python pipeline_manager.py --start_date YYYY-MM-DD --end_date YYYY-MM-DD --crypto [BTC|ETH|SOL|DOGE] --interval [hour|day] --limit <number_of_posts>
```
