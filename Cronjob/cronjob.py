import requests
import json
import datetime
import pandas as pd
import re
from pymongo import MongoClient
from constants import FLAGGED_STRINGS, genes

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

def find_genes(brief_sum, descrip):
     found_genes = []
     split_strings = re.findall(r"[A-Z0-9]+[-]*[A-Z0-9]+", brief_sum + " " + descrip)
     for word in split_strings:
         if word in genes and word not in found_genes:
             found_genes.append(word)
         if '-' in word:
             split_word = re.findall(r"[A-Z0-9]+", word)
             for wrd in split_word:
                 if wrd in genes and wrd not in found_genes:
                     found_genes.append(wrd)
     return found_genes

def find_strings(brief_sum, descrip):
    found_strings = []
    if ("NGS" in brief_sum) or ("NGS" in descrip):
        found_strings.append("NGS")
    for word in FLAGGED_STRINGS:
        if (word in brief_sum.lower()) or (word in descrip.lower()):
            found_strings.append(word)
    return found_strings

def api_getter(date, start_index, size):
    #add more specifications
    url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials"

    # TODO: add payload and use post method instead
    payload = json.dumps({ "record_verification_date_gte": date.strftime("%Y-%m-%d"),
                "size": size,
                "from": start_index,
                "include": ['total', 'record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
                'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id', 'eligibility', 'sites']
    })

    headers = {
        'x-api-key': 'mbxhNtV14K6tiaQ5IUHt2m0wpaKrz9H2cMAz1nHg',
    }
    
    full_data = requests.request("POST", url, headers=headers, data=payload)

    return full_data

def sorting_df(df, nci_id):

    df.sort_values('nci_id', ascending=False, inplace=True)
    df.index = [i for i in range(len(df))]

    new_df = df.where(df['nci_id'] >= nci_id)
    new_df = new_df.dropna(subset=['nci_id'])

    values = {'brief_summary': "", 'detail_description': ""}
    new_df.fillna(value=values)

    gene_list = []
    string_list = []

    for i in range(len(new_df.index)):
        gene_list.append(find_genes(new_df['brief_summary'].iloc[i], new_df['detail_description'].iloc[i]))
        string_list.append(find_strings(new_df['brief_summary'].iloc[i], new_df['detail_description'].iloc[i]))
    new_df['found_genes'] = gene_list
    new_df['found_strings'] = string_list
    
    return new_df    

def get_new_trials():
    # Parameters: date, nci_id
    '''
    Returns a DataFrame containing information about all trials with record verificaiton dates on or after yesterday
    '''

    columns = ['record_verification_date', 'nci_id', 'official_title', 'lead_org', 'current_trial_status', 'start_date',
    'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id', 'eligibility', 'sites']

    data_df = pd.DataFrame(columns=columns)

    nci_id = get_latest_nci_id()
    date = datetime.datetime.today() - datetime.timedelta(days = 14)

    # getting the total
    small_data = api_getter(date, '0', '1').json()
    total = small_data['total']

    for i in range(0, total, 50) :
        full_data = api_getter(date, i, '50').json()
        #checks if api getter gets some kind of data

        print('Total trials:', total)
        print('Current Index:', i)
        print('Percent Completed', str(round(i / total * 100, 1)) + '%')

        if 'data' not in full_data:
            print(full_data)
            break

        for trial in full_data['data']:
            data_df = data_df.append({key: value for key, value in trial.items() if key in columns}, ignore_index=True)

    data_df['sites'] = data_df['sites'].apply(lambda sites: list(set([site['org_country'] for site in sites])) if sites else [])
    data_df['nci_id'] = data_df['nci_id'].apply(lambda id: int(id[4:8] + id[9:]))
    
    # Changes start_date to a date object, can do for other date coluns as well
    #data_df['start_date'] = [datetime.date.fromisoformat(date) for date in data_df['start_date']]
    
    return sorting_df(data_df, nci_id)

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

put_trails()