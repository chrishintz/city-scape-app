from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Pets:

    # @classmethod
    # def chart(self):
    #     pet_score = Pets.average()
    #     return pet_score

    @classmethod
    def average(self):
        week_ago = datetime.today() - timedelta(days = 7)
        pipe = [{"$match": {"module": "Pets", "published_at": {"$gte": week_ago}}},
                {'$group': {'_id': {
                    "dayOfYear": {"$dayOfYear": "$published_at"},
                    "dayOfWeek": {"$dayOfWeek": "$published_at"},
                    "dayOfMonth": {"$dayOfMonth": "$published_at"},
                }, 'total': {'$avg': '$score'}}}, {'$sort': {"published_at.dayOfYear": -1}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        # return list(agg)
        return sorted(list(agg), key = lambda date: date["_id"]["dayOfYear"])

    # @classmethod
    # def recent_average(self, hours=24):
    #     start = datetime.today() - timedelta(hours = hours)
    #     end   = datetime.today()
    #     pipe  = [{"$match": {"module": "Pets",
    #     "published_at": {"$gte": start, "$lte": end}}},
    #     {'$group': {'_id': None, dayOfYear: { '$dayOfYear': "$published_at"},
    #     dayOfWeek: { '$dayOfWeek': "$published_at" }, 'total': {'$avg': '$score'}}}]
    #     agg   = Mongo.collection.aggregate(pipeline=pipe)
    #     return list(agg)

    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Pets"}).sort("published_at", pymongo.DESCENDING)

        if newest_tweet.count() > 0:
            since_id = newest_tweet[0]["tweet_id"]
        else:
            since_id = None

        dog_tweets = Tweet.search(
            "filter:safe seattle dog OR dog's OR dogs OR puppy OR pup OR pooch OR mutt",
            count=1000,
            since_id=since_id
        )
        cat_tweets = Tweet.search(
            "filter:safe seattle cat OR cat's OR cats OR kitty OR kitten OR feline",
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
