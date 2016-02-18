from cityscape.tweet import Tweet

class Influx:
    def __init__(self,tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return ",".join(text)

    @classmethod
    def recent_tweets(self):
        return Influx(Tweet.search("moving to Seattle"))
