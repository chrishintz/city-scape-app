# Create a class
# Search twitter for tweets related to yelling
# Save each relevent tweet in MongoDB with my score
# Allow for researching twitter using the most recent tweet id
# Aggregate data into a single score for a time period
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
        newest_tweet = Mongo.collection.find({"module": "Yell"}).sort("published_at", pymongo.DESCENDING)[0]

        if newest_tweet:
            since_id = newest_tweet["tweet_id"]
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
