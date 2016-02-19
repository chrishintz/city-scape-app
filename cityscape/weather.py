from tweet import Tweet
from mongo import Mongo

class Weather:

    def __init__(self, tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return "<br>".join(text)

    @classmethod
    def save_recent_tweets(self):
        tweets = Tweet.search("weather")
        m = Mongo()
        for t in tweets:
            m.insert_tweet(t)
