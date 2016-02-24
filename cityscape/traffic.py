from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta



class Traffic:

    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Traffic"}}, {
        '$group': {
            '_id': { "month": { "$month": "$published_at" }, "hour": {"$hour": "$published_at"}, "day": {"$dayOfMonth": "$published_at"}, "year": { "$year": "$published_at" }},
            "total": {'$sum': 1 }
        }} ]
        offset = 8
        real_count = []
        count = Mongo.collection.aggregate(pipeline=pipe)
        #only averaging tweets from 6 am to 10 pm
        for everything in count:
            if -2 <= everything["_id"]["hour"]-offset <= 14:
                real_count.append(everything)
        sum = 0
        for hour in real_count:
            if -2 <= hour["_id"]["hour"]-offset <= 14:
                sum += hour["total"]
        return sum/ len(real_count)


    @classmethod
    def recent_average(self, hours=1):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        count = Mongo.collection.find({"published_at": {"$gte": start, "$lte": end} }).count()
        return count

    @classmethod
    def comparison(self):
        return self.recent_average()/self.average()


    @classmethod
    def update_data(self):
        newest_tweet = Mongo.collection.find({"module": "Traffic"}).sort("published_at", pymongo.DESCENDING)
        if newest_tweet.count() > 0:
            since_id = newest_tweet[0]["tweet_id"]
        else:
            since_id = None
        print(since_id)
        tweets = Tweet.search(
        "seattle traffic",
        count=20000,
        since_id=since_id
        )
        for tweet in tweets:
            Mongo.collection.insert_one({
                "module": "Traffic",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": 1
        })


        return True
