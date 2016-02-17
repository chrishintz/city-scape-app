from twython import Twython

class Tweet:

    def __init__(self, dictionary):
        self.text = dictionary["text"]
        self.created_at = dictionary["created_at"]
        self.geo = dictionary["geo"]
        self.id = dictionary["id"]

    @classmethod
    def search(self, term):
        twitter = Twython("", "")
        tweets = twitter.search(q= term)
        new_tweets = []
        for tweet in tweets["statuses"]:
            new_tweets.append(Tweet(tweet))
        return new_tweets
