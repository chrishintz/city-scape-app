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

    def __init__(self, module, published_at, content, tweet_id):
        self.module       = module
        self.published_at = published_at
        self.content      = content
        self.tweet_id     = tweet_id

    @classmethod
    def update_data(self):
        newest_tweets = Mongo.collection.find({"module": "Time"}).sort("published_at", pymongo.DESCENDING)
        newest_tweets = list(newest_tweets)
        if newest_tweets:
            since_id = newest_tweets[0]["tweet_id"]
        else:
            since_id = None

        # collecting all the tweets within specific search terms
        tweets = Tweet.search(
            "-filter:links -filter:retweets geocode:47.609403608607785,-122.35061645507812,300mi",
            count=20000,
            since_id=since_id
        )

        # Go through all of the tweets:
        for tweet in tweets:
            # make instance of Time, assign that to a variable, then call instance methods on it.
            time_instance = Time(
                module       = "Time",
                published_at = tweet.created_at,
                content      = tweet.text,
                tweet_id     = tweet.id
            )

            # use the assign_scores instance method to assign #'s for time-related keywords
            count_dictionary = time_instance.assign_scores()

            # ADDITIONAL INSTANCE METHODS – which need to be specified outside of the update_data() method

                # time_guess = Time.analyze_text(tweet.count_dictionary)
                    # this method gets the highest score from count_dictionary and assigns a time guess

                # check_acuracy = Time.check_accuracy(tweet.time_guess)
                    # compare time guess to published_at

                # time_instance.save()

            # then we update the object in the db with its scores
            Mongo.collection.insert_one({
                "module": time_instance.module,
                "published_at" : time_instance.published_at,
                "content": time_instance.content,
                "tweet_id": time_instance.tweet_id,
                "score": count_dictionary
                # "time_guess": time_guess,
                # "guess_is_accurate": "" - assign as empty string , method below will update to Boolean
            })

        return True

        ##### instance methods:
        ######## (don't need to take arguments)

        # ******** # # ******** # # ******** # # ******** # # ******** #
    def assign_scores(self):
        # each tweet is initialized with an empty hash of keywords related
        # to time, which we're calling 'count dictionary' after initialize/
        # before save...
        keyword_score_dictionary = {}

        for key in Time.dictionary:
            # ...and then each key is assigned to the count dictionary,
            # with a starting value of 0
            keyword_score_dictionary[key] = 0

        # split the tweet's content into a bunch of words, examine each word
        for word in self.content.split():
            # iterate through the dictionary keys...
            for key, value in Time.dictionary.items():
                # if the word appears in the value list...
                if word in value:
                    # add 1 to the score for that key in the dictionary! (for THIS TWEET ONLY)
                    keyword_score_dictionary[key] += 1

        # return the complete hash so that it's available when object is saved in db
        return keyword_score_dictionary

        # the above loop will happen for each word in each tweet,
        # so tweets may have count_dictionaries with scores of
        # multiple 1's, 0's or anything else.

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX INSTANCE METHODS

        # time_guess = Time.analyze_text(self)
            # this method gets the highest score from count_dictionary and assigns a time guess

        # check_acuracy = Time.check_accuracy(self)
            # compare time guess to published_at

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX CLASS METHODS
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
