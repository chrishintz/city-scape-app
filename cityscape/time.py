# Create a class
# Search twitter for tweets related to timeing
# Save each relevent tweet in MongoDB with my score
# Allow for researching twitter using the most recent tweet id
# Aggregate data into a single score for a time period
from cityscape.tweet import Tweet
from cityscape.mongo import Mongo
import pymongo
from datetime import datetime, timedelta

class Time:

    # add @classmethods for score/accuracy later

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Time"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        # collecting all the tweets w/ specific search terms
        tweets = Tweet.search(
            "-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,25mi",
            count=1000,
            since_id=since_id
        )

        # create morning/noon/night categories
        for tweet in tweets:
            # if tweet text contains references to breakfast or sun --> morning_tweets array
                # OPTION A:
                # Mongo.collection.insert_one(
                    # just add new record for this tweet w/ keys for tweet_id and time_guess

                    # then, after all the if/elses determining time of day are done,
                    # UPDATE the same tweet (while still in the 'for' loop w/ remaining attributes
                    # (published_at, content, module) – as these modules apply to all tweets


                # OPTION B:
                    #   for tweet in tweets:
                    #     time_guess = ""
                    #     if tweet has "breakfast"
                    #         time_guess = "breakfast"
                    #     elif tweet has "lunch"
                    #         time_guess = "lunch"

                    # if tweet text contains references to lunch --> daytime_tweets array
                    # repeat for evening
                    # repeat for night
                    # repeat for late night

                    # if it doesn't match any of the time_guess criteria, SKIP saving to MongoDB (explicitly tell Python to do this)

            Mongo.collection.insert_one({
                "module": "Time",
                "published_at": tweet.created_at,
                "content": tweet.text,
                "tweet_id": tweet.id,
                "time_guess": time_guess,
                "guess_is_accurate": ""
                # guess_is_accurate - assign as empty string , method below will update to Boolean
            })

        return True

    # @classmethod
    # def guess_what_time(self):
        # compare count of all tweets from last 3 hours, grouped by time_guess
        # largest count is the educated guess for time of day
        # return output so that it is available in view (i.e. "morning")

    # @classmethod
    # def time_accuracy_check(self):
        # for all the tweets that have been saved in the Time module,
        # update their guess_is_accurate with True or False, based on
        # comparison of time_guess vs published_at
