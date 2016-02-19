from cityscape.tweet import Tweet

class Pets:

    def __init__(self, tweets):
        self.tweets = tweets

    def to_s(self):
        text = []
        for t in self.tweets:
            text.append(t.text)
        return "<br>".join(text)

    @classmethod
    def recent_tweets(self):
        return Pets(Tweet.search("dogs"))
