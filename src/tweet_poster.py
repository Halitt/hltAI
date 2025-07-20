import os
import tweepy
from src.logger import setup_logger, log_info, log_error

from dotenv import load_dotenv
load_dotenv()

setup_logger("tweet_log.txt")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_API_TOKEN = os.getenv("TWITTER_API_TOKEN")

class TwitterPoster:
    def post_tweet(self, text: str):
        newapi = tweepy.Client(
            bearer_token=TWITTER_API_TOKEN,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
        )
        post_result = newapi.create_tweet(text=text)
        if hasattr(post_result, "data") and "id" in post_result.data:
            tweet_id = post_result.data["id"]
            log_info(f"Tweet was sent successfully. id:{tweet_id}")
            return tweet_id

        log_error(f"Failed to send the tweet.")
        return None
        