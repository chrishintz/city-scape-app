# Create a class
# Search twitter for tweets related to Weather
# Save each relevant tweet in MongoDB with my score
# Allow for researching twitter using the most recent tweet id
# Aggregate data into a dingle score for a time period

from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Weather:

    dictionary = {
        "rainy": ["rainy", "raining", "rain", "showers", "drizzle", "drizzling", "sprinkling"],
        "windy": ["windy", "breezy", "wind"],
        "sunny": ["sunny", "sun"],
        "snowy": ["snowy", "snow"],
        "cloudy": ["cloudy", "clouds", "overcast"],
        "thunder": ["thunder"],
        "lightening": ["lightening"]
    }

    @classmethod
    def average(self):
        pipe = [{"$match": {"module": "Weather"}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def recent_average(self):
        start = datetime.today() - timedelta(hours = 24)
        end = datetime.today()
        pipe = [{"$match": {"module": "Weather", "published_at": {"$gte": start, "$lte": end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Weather"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search("-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,6mi", count=100, since_id=since_id)

        for tweet in tweets:
            count_dictionary = {}

            for key in Weather.dictionary:
                count_dictionary[key] = 0

            for word in tweet.text.split():
                for key, value in Weather.dictionary.items():
                    if word in value:
                        count_dictionary[key] += 1

            # percentage = (float(upper_count) / float(len(tweet.text))) * 100
            # if percentage < 20: percentage = 0
            # score = figure out the score for the current weather
            Mongo.collection.insert_one({
                "module": "Weather",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "score": count_dictionary
            })
        return True

    @classmethod
    def current_weather(self):
        total_count_dictionary = {}

        for key in Weather.dictionary:
            total_count_dictionary[key] = 0

        for item in Mongo.collection.find():
            for key, value in item["score"].items():
                total_count_dictionary[key] += value

        print(max(total_count_dictionary, key=total_count_dictionary.get))
        # print(total_count_dictionary)
