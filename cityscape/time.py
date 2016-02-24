# Create a class
# Search twitter for tweets related to timeing
# Save each relevent tweet in MongoDB with my score
# Allow for researching twitter using the most recent tweet id
# Aggregate data into a single score for a time period
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

        # GOAL: assign score for likely time to each tweet
        for tweet in tweets:


            # PASS IN THESE METHODS – which need to be specified outside of the update_data() method
            # count_dictionary = Time.assign_scores(tweet.text)
                # this method needs to return the count_dict containing scores

            # time_guess = Time.analyze_text(tweet.count_dictionary)
                # this method gets the highest score from count_dictionary and assigns a time guess

            # check_acuracy = Time.check_accuracy(tweet.time_guess)
                # compare time guess to published_at


            #each tweet starts with an empty hash of possible time guesses, which we're calling 'count dictionary'
            count_dictionary = {}

            for key in Time.dictionary:
                # and then each key is assigned to the count dictionary, with a starting value of 0
                count_dictionary[key] = 0

                ####### non-regex approach:

            # split the tweet's content into a bunch of words, examine each word
            for word in tweet.text.split():
                # iterate through the dictionary keys...
                for key, value in Time.dictionary.items():
                    # if the word appears in the value list...
                    if word in value:
                        # add 1 to the score for that key in the dictionary! (for THIS TWEET ONLY)
                        count_dictionary[key] += 1

                            # the above loop will happen for each word in each tweet,
                            # so tweets may have count_dictionaries with scores of
                            # multiple 1's, 0's or anything else.

                            # later, make it so that if the entire count_dictionary score is
                            # 0, the tweet isn't even saved in the dictionary.

                    ####### regex approach:
                    # iterate through the dictionary keys...
                    # for key, value_list in Time.dictionary.items():
                    #     # for each value in each list of values belonging to a key
                    #     for value in value_list:
                    #
                    #         if re.search(value, tweet.text.lower()):
                    #             count_dictionary[key] += 1
                    #         # else
                                # skip and do not save in db

                    # FUTURE REFACTOR:  just assign a time_guess to a tweet, skipping assignment
                    # of a bunch of empty scores to each tweet.
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
                "score": count_dictionary
                # "time_guess": time_guess,
                # "guess_is_accurate": ""
                    # guess_is_accurate - assign as empty string , method below will update to Boolean
            })

        return True

        ##### instance methods:
        ######## (don't need to take arguments)
        # count_dictionary = Time.assign_scores(tweet.text)
            # this method needs to return the count_dict containing scores

        # time_guess = Time.analyze_text(tweet.count_dictionary)
            # this method gets the highest score from count_dictionary and assigns a time guess

        # check_acuracy = Time.check_accuracy(tweet.time_guess)
            # compare time guess to published_at



    # add @classmethods for score/accuracy later

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
