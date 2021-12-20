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


