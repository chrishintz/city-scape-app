from twython import Twython
from mongo import Mongo

from django.conf import settings

class Tweet:

    def __init__(self, dictionary):
        self.text = dictionary["text"]
        self.created_at = dictionary["created_at"]
        self.geo = dictionary["geo"]
        self.id = dictionary["id"]

    @classmethod
    def search(self, term):

        twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)

        tweets = twitter.search(q = term)
        new_tweets = []
        for tweet in tweets["statuses"]:
            new_tweets.append(Tweet(tweet))
        return new_tweets
