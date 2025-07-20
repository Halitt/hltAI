from src.tweet_manager import TweetManager
from src.tweet_poster import TwitterPoster

def sendTweet():
    tweet_manager = TweetManager()
    twitter_poster = TwitterPoster()
    first_tweet = tweet_manager.get_first_tweet()
    if first_tweet is not None:
        cleanedText = first_tweet["content"].strip('"')
        res = twitter_poster.post_tweet(cleanedText)
        if res is not None:
            tweet_manager.find_and_delete(first_tweet["id"])

sendTweet()