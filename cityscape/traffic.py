from twython import Twython
from django.conf import settings
import Algorithmia
import time
from cityscape.tweet import Tweet

print (time.strftime("%Y/%m/%d"))
time = (time.strftime("%Y/%m/%d"))

input = "Karen"
client = Algorithmia.client('simA/10GUxSaf8N3a8CWDf6LKmd1')
algo = client.algo('demo/Hello/0.1.1')
print (algo.pipe(input))


class Traffic:

    def __init__(self, tweets):
        self.tweets = tweets


    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return ",".join(text)

    @classmethod
    def search(self, term):
        self.time = time.strftime("%Y/%m/%d")
        # term = "lang:en -filter:retweets -filter:links traffic seattle since:\n{self.time}."
        term = "lang:en -filter:retweets -filter:links traffic seattle."
        twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
        tweets = twitter.search(q = term, result_type = "recent", count= 1000)
        new_tweets = []
        for tweet in tweets["statuses"]:
            new_tweets.append(Traffic(tweet))
        # input = new_tweets[1].text
        # client = Algorithmia.client('simA/10GUxSaf8N3a8CWDf6LKmd1')
        # algo = client.algo('StanfordNLP/SentimentAnalysis/0.1.0')
        # print (algo.pipe(input))
        # return (algo.pipe(input))
        return new_tweets
        return len(new_tweets)

    @classmethod
    def recent_tweets(self):
        # time = time.strftime("%Y/%m/%d")
        return Traffic(Tweet.search("lang:en -filter:retweets -filter:links traffic seattle since:\n{time}."))
