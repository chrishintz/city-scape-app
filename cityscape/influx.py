from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Influx:
    @classmethod
    def recent_count(self, hours = 720):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [{"$match": {"module": "Influx", "published_at": {"$gte": start, "$lte": end}}}]
        day_count = Mongo.collection.count(pipeline = pipe)
        return day_count

    @classmethod
    def average(self, hours=8640):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [
            {"$match": {"module": "Influx", "published_at": {"$gte": start, "$lte": end}}},
            {'$group': {'_id': {"month": {"$month": "$published_at"}}, 'total': {'$sum': 1}}}
        ]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return len(list(agg))
        # how to count object that's insides the array....elements of the object inside an array?

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Influx"}).sort("published_at", pymongo.DESCENDING)
        if newest_tweets.count() > 0:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search("filter:safe -filter:retweets -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'",count = 20000, since_id=since_id)
        for tweet in tweets:

            Mongo.collection.insert_one({
                "module": "Influx",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
            # "score": percentage
            })
        return len(tweets)

    @classmethod
    def score(self):
        if self.recent_count() > self.average():
            print("The Amount of People Moving to Seattle is Higher Than Average")
        else:
            print("The Amount of People Moving to Seattle is Lower Than Normal")
