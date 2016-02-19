from twython import Twython
from django.conf import settings
import tweepy

class Tweet:
    #
    # def __init__(self, dictionary):
    #     self.text = dictionary["text"]
    #     self.created_at = dictionary["created_at"]
    #     self.geo = dictionary["geo"]
    #     self.id = dictionary["id"]

    @classmethod
<<<<<<< HEAD
    def search(self, term):
        twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        tweets = twitter.search(q= term, result_type = "recent", count= 1000)
=======
    def search(self, term, count=100, since_id=None):
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)

        # construct the API instance
        api = tweepy.API(auth)

        tweets = tweepy.Cursor(api.search, q= term, since_id=since_id).items(count)

>>>>>>> 223db0a2fcbac668667608e9bbc031b69e6ae54f
        new_tweets = []
        for tweet in tweets:
            new_tweets.append(tweet)
        return new_tweets
