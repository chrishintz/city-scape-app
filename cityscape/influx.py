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
        return list(agg)[0]['total']


    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Influx"}).sort("published_at", pymongo.DESCENDING)
        if newest_tweets.count() > 0:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search("filter:safe since:2014-12-21 -filter:retweets -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'",count = 20000, since_id=since_id)
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
        recent_count = self.recent_count()
        average = self.average()
        # %s replaces this value with the following value outside of the string
        print ("The Current 6 Month Average of People Moving to Seattle, Based on Twitter Data is: %s" %average)
        if recent_count > average:
            print("The Amount of People Moving to Seattle is Higher Than Normal: Current Count = %s" %recent_count)
        elif recent_count < average:
            print("The Amount of People Moving to Seattle is Lower Than Normal: Current Count   = %s" %recent_count)
        else:
            print("The Amount of People Moving to Seattle is the Same as Normal: Current Count = %s" %recent_count)
            return recent_count
