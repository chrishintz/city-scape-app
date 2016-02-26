from cityscape.tweet import Tweet

class Yell:

    def __init__(self, tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return ",".join(text)

    @classmethod
    def recent_tweets(self):
        return Yelling(Tweet.search("yelling"))





# t = Tweet.search("lang:en -filter:retweets -filter:links Tacos seattle")
#
#
# t = Tweet.search("lang:en -filter:retweets -filter:links traffic seattle since:2016-02-17")
