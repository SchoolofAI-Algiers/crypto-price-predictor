# 🚀 Cryptocurrency Price Prediction Pipeline

## 📌 Overview
This project is a **cryptocurrency data pipeline** that fetches historical price data from Binance, preprocesses it, and saves it for further analysis and model training.

## 🏗 Project Structure
```bash
Cryptocurrency_Prediction/
|--- src/                     # Source code
|    |--- components/          # Data pipeline components
|    |    |--- data_fetcher.py  # Fetches historical data from Binance API
|    |    |--- data_preprocessor.py # Cleans and prepares the data
|    |    |--- model_trainer.py # Model training (if applicable)
|    |--- utils/               # Utility functions
|    |    |--- helpers.py       # Helper functions
|    |--- logs/                # Log files (auto-generated daily)
|    |--- exception.py         # Custom exception handling
|    |--- logger.py            # Logger setup
|--- artifacts/               # Processed data and saved models
|--- pipeline_manager.py      # Main script to run the pipeline
|--- requirements.txt         # Required Python dependencies
|--- README.md                # Project documentation
|--- .gitignore               # Files to ignore in Git
```


## 📥 Installation
To set up the project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/SelmaKhelili/Cryptocurrency_Prediction.git

# Navigate into the project directory
cd Cryptocurrency_Prediction

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
## 🚀 Usage
Run the pipeline using:
```bash
python pipeline_manager.py --coin_name bitcoin --interval 1h --limit 500
```
- `Arguments` : 
Argument	Type	Description	Default
--coin_name	string	Name of the cryptocurrency (e.g., bitcoin, ethereum)	Required
--interval	string	Time interval (1m, 1h, 1d, etc.)	1d
--limit	int	Number of data points to fetch	365

## 📊 Features

    ✅ Fetches real-time cryptocurrency data from Binance.
    ✅ Preprocesses raw data into a structured format.
    ✅ Stores cleaned data in a CSV file for further analysis.
    ✅ Logs execution details into a logs/ folder with daily log files.

## 🛠 Configuration
Modify logger.py to customize log storage or levels.
```bash
log_file = os.path.join(log_dir, f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log")
```

