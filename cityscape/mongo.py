from pymongo import MongoClient

class Mongo:

    # connecting code below to mongo database server
    client = MongoClient()
    # tells mongo database server to create new database called 'test_database'
    # mongo server returns database object called 'db'
    db = client['cityscape']
    # tells mongo database server to create new collection (a.k.a. table) called 'test_collection' inside 'test_database'
    # mongo server returns collection object called 'collection'
    collection = db['tweet_stats']

    def insert_tweet(self, tweet):
        collection.insert_one({"tweet_id": tweet.id, "created_at": tweet.created_at, "tweet_text": tweet.text})
