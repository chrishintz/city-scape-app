# create a class
# search twitter for yelling related tweets
# save each relevent tweet in mongodb with myscore
# allow for researching twitter using most recent tweet id
# aggregate data into a single score for time period



from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Yell:


    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Yell"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def recent_average(self, hours=24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [{"$match": {"module": "Yell", "published_at": {"$gte": start, "$lte": end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)


    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Yell"}).sort("published_at", pymongo.DESCENDING)

        if len(list(newest_tweet)) > 0:
            since_id = newest_tweet[0]["tweet_id"]
        else:
            since_id = None

        print(since_id)
        tweets = Tweet.search(
            "-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,25mi",
            count=1000,
            since_id=since_id
        )
        for tweet in tweets:
            upper_count = 0
            for char in list(tweet.text):
                if 65 <= ord(char) <= 90:
                    upper_count += 1
            percentage = (float(upper_count) / float(len(tweet.text))) * 100
            if percentage < 20: percentage = 0
            # score = figure out the count chars uppercase
            Mongo.collection.insert_one({
                "module": "Yell",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": percentage
            })
        return True



    # def __init__(self, tweets):
    #     self.tweets = tweets
    #
    # def to_s(self):
    #     text = []
    #     for t in self.tweets:
    #         text.append(t.text)
    #     return ",".join(text)
    #
    # @classmethod
    # def recent_tweets(self):
    #     return Yelling(Tweet.search("yelling"))




# t = Tweet.search("lang:en -filter:retweets -filter:links Tacos seattle")
#
#
# t = Tweet.search("lang:en -filter:retweets -filter:links traffic seattle since:2016-02-17")
