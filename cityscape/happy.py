from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta
from cityscape.algorithm import Algorithm


class Happy:

    # algo_path = 'nlp/SentimentAnalysis/0.1.2'
    algo_path = 'mtman/SentimentAnalysis/0.1.1'


    @classmethod
    def chart(self):
        ans = Happy.recent_average(1.5)[0]["total"] + 1
        percentage = ans/2 * 100
        # percentage = 20
        emptiness = 100 - percentage
        image = ""
        if percentage < 50:
            image = "sad.png"
        elif percentage < 60 and percentage > 50:
            image = "neutral.png"
        else:
            image = "happy.png"
        return {"percentage": percentage, "emptiness": emptiness, "image": image}

    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Happy"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def recent_average(self, hours=24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [{"$match": {"module": "Happy", "published_at": {"$gte": start, "$lte": end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Happy"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search(
                "-filter:links lang:en -filter:retweets geocode:47.609403608607785,-122.35061645507812,16mi",
                count=10000,
                since_id=since_id
                )

        for tweet in tweets:
            tw = tweet.text.encode("latin-1", "ignore").decode("latin-1")
            algo_score = Algorithm.search(tw, self.algo_path)
            Mongo.collection.insert_one({
                "module": "Happy",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": algo_score
            })

        return True

