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
thumbnails = db["News_Thumbnails"]
headlines = db["Headlines"]
meta_info = db["More_info"]

def store_news(data):
    """Stores scraped news data in MongoDB."""
    for story in data:
        thumbnails.insert_one({"image": story["image"]})
        headlines.insert_one({"Headline": story["headline"]})
        meta_info.insert_one({
            "Article_link": story["url"],
            "Date_of_Article": story["article_date"],
            "ArticleScrapeTime": story["scrape_time"]
        })
