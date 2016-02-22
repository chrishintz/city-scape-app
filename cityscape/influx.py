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

    def average(self, hours=24):
        start = datetime.today() - timedelta(hours = hours)
        end   = datetime.today()
        pipe = [{"$match": {"module": "Influx", "published_at": {"$gte": start, "$lte": end}}}, {'$group': {'_id': None, 'total': {'$avg': '$score'}}}]
        agg = Mongo.collection.aggregate(pipeline=pipe)
        return list(agg)

    def recent_tweets(self):
        tweets = Influx(Tweet.search("filter:safe -filter:retweets -if -? -considering -consideration -thinking -may  -filter:links 'moving to seattle'",count = 100,))
        for tweet in tweets:
            tweet.created_at,
            tweet.text,
            tweet.id,

            # upper_count = 0
            # for char in list(tweet.text):
            #     if 65 <= ord(char) <= 90:
            #         upper_count += 1
            # percentage = (float(upper_count) / float(len(tweet.text))) * 100
            # if percentage < 20: percentage = 0

        Mongo.collection.insert_one({
            "module": "Yell",
            "published_at": tweet.created_at,
            "content": tweet.text,
            "tweet_id": tweet.id,
            # "score": percentage
        })
