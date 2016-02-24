{from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta
import re

class Weather:

    dictionary = {
        "rainy": ["rainy", "raining", "rain", "showers", "drizzle", "drizzling", "sprinkling"],
        "windy": ["windy", "breezy", "wind", "winds"],
        "sunny": ["sunny", "sun", "partly cloudy"],
        "snowy": ["snowy", "snow"],
        "cloudy": ["cloudy", "clouds", "overcast"],
        "thunder": ["thunder"],
        "lightening": ["lightening"]
    }

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Weather"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search("-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,6mi", count=20000, since_id=since_id)

        for tweet in tweets:
            count_dictionary = {}

            for key in Weather.dictionary:
                count_dictionary[key] = 0

            # without regex
            # for word in tweet.text.split():
            #     for key, value in Weather.dictionary.items():
            #         if word in value:
            #             count_dictionary[key] += 1

            # with regex
            for key, value_list in Weather.dictionary.items():
                for value in value_list:
                    if value == "wind":
                        wind_mph = Weather.extract_wind_in_mph(tweet.text.lower())

                        # increment count only if wind is above threshhold
                        if (25 <= wind_mph):
                            count_dictionary[key] += 1
                    else:
                        if re.search(value, tweet.text.lower()):
                            count_dictionary[key] += 1

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

        for item in Mongo.collection.find({"published_at": {"$gte": datetime.today() - timedelta(hours = 3)}}):
            for key, value in item["score"].items():
                total_count_dictionary[key] += value

        return max(total_count_dictionary, key=total_count_dictionary.get)
        # print(total_count_dictionary)

    @classmethod
    def extract_wind_in_mph(self, tweet_content):
        result = re.search("wind (.+?)mph", tweet_content)

        if result:
            return int(result.group(1))
        else:
            return 0
