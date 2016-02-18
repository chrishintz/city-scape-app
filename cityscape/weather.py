# from cityscape.tweet import tweet
#
# class Weather:
#
#     def __init__(self, tweets):
#         self.tweets = tweets
#
#     def to_s(self):
#         text = []
#         for t in self.tweets:
#             text.append(t.text)
#         return "<br>".join(text)
#
#     @classmethod
#     def recent_tweets(self):
#         return Weather(Tweet.search("weather"))
