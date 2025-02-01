from modules.scraper import get_top_stories
from modules.storage import store_news
from modules.deduplication import is_duplicate
from modules.logger import log_info, log_error
import pymongo
import json

# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

DB_URI = config["database"]["uri"]
DB_NAME = config["database"]["db_name"]

# Connect to MongoDB
client = pymongo.MongoClient(DB_URI)
db = client[DB_NAME]
meta_info = db["More_info"]

try:
    log_info("Pipeline started.")

    # Step 1: Scrape News
    news_data = get_top_stories()
    log_info(f"Scraped {len(news_data)} articles.")

    # Step 2: Deduplication Check
    filtered_data = [story for story in news_data if not is_duplicate(story, meta_info)]
    log_info(f"{len(filtered_data)} new articles to store.")

    # Step 3: Store in Database
    store_news(filtered_data)

    log_info("Pipeline completed successfully.")

except Exception as e:
    log_error(f"Pipeline error: {e}")
