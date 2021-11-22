from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://upsync:upsync@cluster0.p5teq.mongodb.net/test"

def update_latest_nci_id(nci_id):

    client = MongoClient(CONNECTION_STRING)
    trials_db = client['burning_rock_db_v2']
    trials = trials_db['latest']
    trials.delete_many({})
    trials.insert_one({'nci_id': nci_id})

def get_latest_nci_id():
    client = MongoClient(CONNECTION_STRING)
    trials_db = client['burning_rock_db_v2']
    trials = trials_db['latest']
    nci_id = trials.find_one()
    return nci_id['nci_id']

def put_trails():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    trials_db = client['burning_rock_db_v2']

    # Creates a collection in the trials database
    trials = trials_db['trials']

    # CHANGE THIS: assign trials_df to a dataframe of accessed trials
    new_trials = get_new_trials()
    
    if not new_trials.empty:
        max_nci = max(new_trials['nci_id'])
        update_latest_nci_id(max_nci)
        # Adds to the trials collections
        trials.insert_many(new_trials.to_dict('records'))
