import os
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

GOOGLE_NEWS_URL = config["google_news_url"]
TOP_STORIES_TEXT = config["top_stories_text"]

def get_top_stories():
    """Scrape top stories from Google News."""
    driver = webdriver.Chrome()
    driver.get(GOOGLE_NEWS_URL)

    try:
        # Click on "Top Stories" dynamically
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, TOP_STORIES_TEXT))).click()

        # Extract story elements
        story_tags = driver.find_elements(By.TAG_NAME, "c-wiz")

        data = []
        story_count = 0
        image_folder = "news_images"
        os.makedirs(image_folder, exist_ok=True)

        for story in story_tags:
            if story.get_attribute("class") == "PO9Zff Ccj79 kUVvS":
                story_count += 1

                # Extract Image
                img_url = None
                image_tags = story.find_elements(By.TAG_NAME, "img")
                for img in image_tags:
                    if img.get_attribute("class") == "Quavad vwBmvb":
                        img_url = img.get_attribute("src")
                        break

                # Download Image
                image_path = None
                if img_url:
                    response = requests.get(img_url, stream=True)
                    if response.status_code == 200:
                        image_path = os.path.join(image_folder, f"news_{story_count}.jpg")
                        with open(image_path, "wb") as img_file:
                            img_file.write(response.content)

                # Extract Headline & Metadata
                headline = story.find_element(By.CLASS_NAME, "gPFEn").text
                article_url = story.find_element(By.TAG_NAME, "a").get_attribute("href")
                article_date = story.find_element(By.TAG_NAME, "time").get_attribute("datetime")

                # Store Metadata
                data.append({
                    "headline": headline,
                    "image": image_path,
                    "url": article_url,
                    "scrape_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "article_date": article_date
                })

                time.sleep(2)  # Lazy loading

        driver.quit()
        return data

    except Exception as e:
        driver.quit()
        print(f"Scraping error: {e}")
        return []
