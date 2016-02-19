# Create a class
# Search twitter for tweets related to yelling
# save each relevant tweet in MongoDb with my score
# Allow for researching twiter using the most recent tweet id
# Aggregate data into a single score for a time period
from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
import datetime

class Yelling:
# intialize around a list of tweets if wanted
    def __init__(self,tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return ",".join(text)

    @classmethod
    def recent_tweets(self):
        tweet =Yelling(Tweet.search("filter:safe -filter:retweets -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'",count = 100,))
        return tweet
        # return Yelling(Tweet.search("filter:safe Yelling"))
