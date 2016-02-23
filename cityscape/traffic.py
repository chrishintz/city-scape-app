from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta


class Traffic:

    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Traffic"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def recent_average(self, hours=24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [{"$match": {"module": "Traffic", "published_at": {"$gte": start, "$lte": end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)


    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Traffic"}).sort("published_at", pymongo.DESCENDING)
        if newest_tweet:
            since_id = newest_tweet[0]["tweet_id"]
        else:
            since_id = None
        print(since_id)
        tweets = Tweet.search(
        "seattle traffic -filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,25mi",
        count=1000,
        since_id=since_id
        )
        # count = len(tweets)
        for tweet in tweets:

            Mongo.collection.insert_one({
                "module": "Traffic",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": 1
        })

        return True
