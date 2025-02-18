import logging
import os
from datetime import datetime

def get_logger():
    # Ensure logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Generate log file name based on the current date
    log_file = os.path.join(log_dir, f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log")

    # Create a logger
    logger = logging.getLogger("CryptoPipeline")
    logger.setLevel(logging.INFO)

    # Formatter for logs
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler (logs will be saved in 'logs/pipeline_YYYY-MM-DD.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Stream handler (logs will also appear in the console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
