# Create a class
# Search twitter for tweets related to yelling
# save each relevant tweet in MongoDb with my score
# Allow for researching twiter using the most recent tweet id
# Aggregate data into a single score for a time period
from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
import datetime

class Yell:

    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Yell"}).sort(“published_at”, pymongo.DESCENDING)[0]
        if newest_tweet:
            since_id = newest_tweet["tweet_id"]
        else:
             since_id = None
        tweets = Tweet.search(
        "-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,6mi",
        count = 200,
        since_id =since_id)
        # print(tweets)
        for tweet in tweets:
            upper_count = 0
            for char in list(tweet.text):
                if 65 <= ord(char) <=90:
                    upper_count += 1
            percentage = (float(upper_count) / float(len(tweet.text))) * 100
            if percentage < 20: percentage = 0
            # score = figure out the count of chars uppercase
            Mongo.collection.insert_one({
            # can search by a specific module in the database with "yell"
                "module": "Yell",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": score,
            })
        return True

        @classmethod
        def average(self):
            pipe = [{"$match": {"module": "Yell"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
            agg = Mongo.collection.aggregate(pipeline = pipe)
            return list(agg)

        @classmethod
        def average(self, hours = 24):
            start = datetime.today() - timedelta(hours = 24)
            end = datetime.today()
            pipe = [{"$match": {"module": "Yell", "published_at": {"$gte" start, "$lte":end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
            # gte = "greater than", lte = less than
            agg = Mongo.collection.aggregate(pipeline = pipe)
            return list(agg)


# from cityscape.tweet import Tweet
#
# class Yelling:
# # intialize around a list of tweets if wanted
#     def __init__(self,tweets):
#         self.tweets = tweets
#
#     def to_s(self):
#         text = []
#         for t in self.tweets:
#             text.append(t.text)
#         return ",".join(text)
#
#     @classmethod
#     def recent_tweets(self):
#         # return Yelling(Tweet.search("filter:safe -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'", count = 100,))
#         return Yelling(Tweet.search("filter:safe Yelling"))
