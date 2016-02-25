from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Influx:
    @classmethod
    def recent_count(self, hours = 24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        day_count = Mongo.collection.find({ "published_at": {"$gte": start, "$lte": end}}).count()
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

        tweets = Tweet.search("filter:safe -filter:retweets -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'",count = 20000, since_id=since_id)
        for tweet in tweets:

            Mongo.collection.insert_one({
                "module": "Influx",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
            })
        return len(tweets)

    @classmethod
    def score(self):
        recent_count = self.recent_count()
        update_data = self.update_data
        average = (self.average()/10)
        #tweepy counts 10 days in past
        # %s replaces this value with the following value outside of the string
        # return("The Current 10 Day Average of People Moving to Seattle (Based on Twitter Data) is: %s" %average)
        return average

    @classmethod
    def score_calc(self):
        recent_count = self.recent_count()
        average = (self.average()/10)

        if recent_count > average:
            return("The Amount of People Moving to Seattle Today is Higher Than Normal: Current Count = %s" %recent_count)
        elif recent_count < average:
            return("The Amount of People Moving to Seattle is Lower Than Normal: Current Count  = %s" %recent_count)
        else:
            return("The Amount of People Moving to Seattle is the Same as Normal: Current Count = %s" %recent_count)
