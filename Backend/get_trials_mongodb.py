from pymongo import MongoClient
import pymongo
from bson.json_util import dumps

def get_database():

    CONNECTION_STRING = "mongodb+srv://upsync:upsync@cluster0.p5teq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)

    return client['burning_rock_db_v2']


# This is added so that many files can reuse the function get_database()
def get_trials_from_db(): 
    
    # Get the database
    dbname = get_database()

    trials_collection = dbname['trials']

    #sort by descending for newest trials first
    sorted_trials = trials_collection.find({}).sort('nct_id', pymongo.DESCENDING).limit(100)

    return dumps(sorted_trials)


