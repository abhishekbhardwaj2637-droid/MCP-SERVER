import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

# Ensure data directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Application Config
APP_PACKAGE_NAME = os.getenv("APP_PACKAGE_NAME", "com.nextbillion.groww")
REVIEW_TIME_WINDOW_WEEKS = int(os.getenv("REVIEW_TIME_WINDOW_WEEKS", "12"))
MAX_REVIEWS_TO_FETCH = int(os.getenv("MAX_REVIEWS_TO_FETCH", "5000"))

# Default language and country for scraping
SCRAPER_LANG = os.getenv("SCRAPER_LANG", "en")
SCRAPER_COUNTRY = os.getenv("SCRAPER_COUNTRY", "in")
