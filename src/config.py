import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/trading_db")

# API configuration
API_PREFIX = ""  # Root path
API_TITLE = "Trading Strategy API"
API_DESCRIPTION = "API for stock data and trading strategy analysis"
API_VERSION = "1.0.0"

# Moving average strategy configuration
SHORT_WINDOW = int(os.getenv("SHORT_WINDOW", "5"))  # 5-day moving average
LONG_WINDOW = int(os.getenv("LONG_WINDOW", "20"))   # 20-day moving average