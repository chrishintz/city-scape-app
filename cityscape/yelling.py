from cityscape.tweet import Tweet

class Yelling:
# intialize around a list of tweets if wanted
    def __init__(self,tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return ",".join(text)

    @classmethod
    def recent_tweets(self):
        return Yelling(Tweet.search("filter:safe -if -? -considering -consideration -thinking -filter:links moving to seattle"))
