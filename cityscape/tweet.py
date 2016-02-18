from twython import Twython
from django.conf import settings
import tweepy

class Tweet:

    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)

    # construct the API instance
    api = tweepy.API(auth)

    public_tweets = api.search(q = 'seattle tacos')
    # limit # of iterations through statuses
    for status in tweepy.Cursor(api.search, q='tacos').items(200):
        print(status.text)

    # def __init__(self, dictionary):
    #     self.text = dictionary["text"]
    #     self.created_at = dictionary["created_at"]
    #     self.geo = dictionary["geo"]
    #     self.id = dictionary["id"]
    #     self.location = dictionary["location"]
    #
    # @classmethod
    # def search(self, term):
    #     twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    #     tweets = twitter.cursor(twitter.search, q= term, count= 100, result_type='recent', since_id='700120196539744256')
    #     i = 0
    #     for tweet in tweets:
    #         i += 1
    #         print(tweet)
    #         print(i)


        # new_tweets = []
        # for tweet in tweets["statuses"]:
        #     new_tweets.append(Tweet(tweet))
        # return new_tweets
