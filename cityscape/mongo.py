from pymongo import MongoClient
import os

class Mongo:

    # connecting code below to mongo database server
    if os.environ.get("MONGOLAB_URI"):
        client = MongoClient(os.environ.get("MONGOLAB_URI"))
        db = client['heroku_bw0c99x4']
    else:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['cityscape']


    # mongolab_uri = os.environ.get("MONGOLAB_URI")
    # tells mongo database server to create new database called 'test_database'
    # mongo server returns database object called 'db'

    # tells mongo database server to create new collection (a.k.a. table) called 'test_collection' inside 'test_database'
    # mongo server returns collection object called 'collection'
    collection = db['tweet_stats']

    def insert_tweet(self, tweet):
        collection.insert_one({"tweet_id": tweet.id, "created_at": tweet.created_at, "tweet_text": tweet.text})
