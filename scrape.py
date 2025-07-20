import asyncio
from typing import List
from src.rss_reader import RSSReader
from src.scraper import Scraper
from src.ai_analyzer import AIAnalyzer
from src.tweet_manager import TweetManager
from src.logger import setup_logger, log_info, log_error
import time

setup_logger("scrape_log.txt")

async def scrape():
    feed_url = "https://cointelegraph.com/rss"
    urls = fetch_urls(feed_url)
    if not urls:
        log_info("No new articles found.")
        return

    markdowns = await scrape_articles(urls)
    await process_markdowns(markdowns)

def fetch_urls(feed_url: str) -> List[str]:
    rss_reader = RSSReader(feed_url)
    return rss_reader.fetch_latest()

async def scrape_articles(urls: List[str]) -> List[str]:
    scraper = Scraper(urls)
    return await scraper.scrape()

async def process_markdowns(markdowns: List[str]):
    tweet_manager = TweetManager()
    analyzer = AIAnalyzer()
    for markdown in markdowns:
        try:
            tweet = analyzer.summarize(markdown)
            if "No tweet needed" not in tweet:
                milliseconds = str(int(time.time() * 1000))
                tweet_manager.write_tweet(milliseconds, tweet)
            await asyncio.sleep(10)
        except Exception as e:
            log_error(f"Error processing article: {e}")

asyncio.run(scrape())