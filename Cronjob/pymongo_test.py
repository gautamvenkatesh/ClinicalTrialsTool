from pymongo import MongoClient
import pymongo
import pandas as pd
import cronjob

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://upsync:upsync@cluster0.p5teq.mongodb.net/test"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
trials_db = client['trials_db']

# Creates a collection in the trials database
trials = trials_db['trials']

# CHANGE THIS: assign trials_df to a dataframe of accessed trials
new_trials = cronjob.get_new_trials()

# Adds to the trials collections
trials.insert_many(new_trials.to_dict('records'))