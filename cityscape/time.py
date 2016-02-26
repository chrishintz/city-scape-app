from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta
import re

class Time:

    dictionary = {
        "early":     ["early","insomnia"],
        "morning":   ["morning", "breakfast", "awake"],
        "afternoon": ["afternoon","lunch"],
        "evening":   ["night", "dinner", "tired"],
        "late" :     ["midnight","dark"]
    }

    def __init__(self, module, published_at, content, tweet_id, score = None, time_guess = None, actual_timeframe = None, accurate_guess = None):
        self.module           = module
        self.published_at     = published_at
        self.content          = content
        self.tweet_id         = tweet_id
        self.score            = score
        self.time_guess       = time_guess
        self.actual_timeframe = actual_timeframe
        self.accurate_guess   = accurate_guess


    @classmethod
    def find(self, tweet_id):
        self.tweet_id = tweet_id

        instance = Mongo.collection.find_one({"module":"Time", "tweet_id": tweet_id})
        t = Time(
            module           = "Time",
            published_at     = instance["published_at"],
            content          = instance["content"],
            tweet_id         = instance["tweet_id"],
            score            = instance["score"],
            time_guess       = instance["time_guess"],
            actual_timeframe = instance["actual_timeframe"],
            accurate_guess   = instance["accurate_guess"]
        )
        return t

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Time"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        tweets = Tweet.search(
            "-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,300mi",
            count=1000,
            since_id=since_id
        )

        for tweet in tweets:
            time_instance = Time(
                module       = "Time",
                published_at = tweet.created_at,
                content      = tweet.text,
                tweet_id     = tweet.id
            )

            time_instance.assign_scores()

            time_instance.compute_time_guess()

            time_instance.check_accuracy()

            # time_instance.save()

            # then we update the object in the db with its scores
            Mongo.collection.insert_one({
                "module":           time_instance.module,
                "published_at" :    time_instance.published_at,
                "content":          time_instance.content,
                "tweet_id":         time_instance.tweet_id,
                "score":            time_instance.score,
                "time_guess":       time_instance.time_guess,
                "actual_timeframe": time_instance.actual_timeframe,
                "accurate_guess":   time_instance.accurate_guess
            })

        return True

    # @classmethod
    # def guess_what_time(self):
        # compare count of all tweets from last 3 hours, grouped by time_guess
        # largest count is the educated guess for time of day
        # return output so that it is available in view (i.e. "morning")

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX INSTANCE METHODS

    def assign_scores(self):
        keyword_score_dictionary = {}

        for key in Time.dictionary:
            keyword_score_dictionary[key] = 0

        for word in self.content.split():
            for key, value in Time.dictionary.items():
                if word in value:
                    keyword_score_dictionary[key] += 1

        self.score = keyword_score_dictionary

    # this method gets the highest score from count_dictionary and assigns a time guess
    def compute_time_guess(self):
        v = list(self.score.values())
        k = list(self.score.keys())
        maxv = max(v)
        if maxv > 0:
            self.time_guess = k[v.index(max(v))]

    def check_accuracy(self):
        # this converts the published_at time to an integer; -8 is UTC to PST
        # conversion – so this would have to be updated later for other timezones.
        pub_hour = self.published_at.hour - 8

        if 0 <= pub_hour < 4:
            self.actual_timeframe = "late"
        elif 4 <= pub_hour < 6:
            self.actual_timeframe = "early"
        elif 6 <= pub_hour < 12:
            self.actual_timeframe = "morning"
        elif 12 <= pub_hour < 18:
            self.actual_timeframe = "afternoon"
        else:
            self.actual_timeframe = "night"

        if self.actual_timeframe == self.time_guess:
            self.accurate_guess = True
        else:
            self.accurate_guess = False
