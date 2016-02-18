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
