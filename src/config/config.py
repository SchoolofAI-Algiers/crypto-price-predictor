import os
from datetime import datetime

# Base configuration
BASE_URL = "https://finance.yahoo.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'data')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')

# Ensure directories exist
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Logging configuration
LOG_FILE = os.path.join(LOGS_DIR, f'scraper_{datetime.now().strftime("%Y%m%d")}.log')
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}