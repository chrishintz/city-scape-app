from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Pets:

    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Pets"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def recent_average(self, hours=24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe  = [{"$match": {"module": "Pets", "published_at": {"$gte": start, "lte": end}}}, {'group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg   = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Pets"}).sort("published_at", pymongo.DESCENDING)

        if newest_tweet.count() > 0:
            since_id = newest_tweet[0]["tweet_id"]
        else:
            since_id = None

        print(since_id)
        dog_tweets = Tweet.search(
            "seattle dog OR dogs seattle OR dog's seattle OR puppy seattle OR pooch seattle OR mutt seattle",
            count=1000,
            since_id=since_id
        )
        cat_tweets = Tweet.search(
            "seattle cat OR cats seattle OR cat's seattle OR kitty seattle OR kitten seattle OR feline seattle",
            count=1000,
            since_id=since_id
        )
        for tweet in dog_tweets:
            Mongo.collection.insert_one({
                "module": "Pets",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": 1
            })
        for tweet in cat_tweets:
            Mongo.collection.insert_one({
                "module": "Pets",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": -1
            })
        return True
