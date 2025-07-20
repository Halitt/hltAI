from tinydb import TinyDB, Query

class TweetManager:
    def __init__(self, db_path='tweets.json'):
        self.db = TinyDB(db_path)
        self.tweet_table = self.db.table('tweets')

    def write_tweet(self, tweet_id: str, content: str):
        self.tweet_table.insert({'id': tweet_id, 'content': content})

    def delete_tweet(self, tweet_id: str):
        Tweet = Query()
        self.tweet_table.remove(Tweet.id == tweet_id)

    def find_tweet(self, tweet_id: str):
        Tweet = Query()
        result = self.tweet_table.search(Tweet.id == tweet_id)
        return result[0] if result else None
    
    def all(self):
        all_tweets = self.tweet_table.all()
        return all_tweets
    
    def get_first_tweet(self):
        all_tweets = self.tweet_table.all()
        return all_tweets[0] if all_tweets else None
    
    def find_and_delete(self, tweet_id: str):
        tweet = self.find_tweet(tweet_id)
        if tweet is not None:
            self.delete_tweet(tweet_id)
