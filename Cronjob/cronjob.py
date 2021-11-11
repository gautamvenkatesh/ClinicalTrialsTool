import requests
import json
import datetime
import pandas as pd
from Utils import *

def api_getter(date, start_index, size):
    #add more specifications
    url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=" + size + "&record_verification_date=" + date
    url += '&from=' + str(start_index)

    # TODO: add payload and use post method instead
    payload = json.dumps({ "record_verification_date_gte": date,
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
    if len(nci_id) == 15:
        nci_id = nci_id.str[4:8] + df['nci_id'].str[9:14]

    df.sort_values('nci_id', ascending=False, inplace=True)
    df.index = [i for i in range(len(df))]


    df['nci_id_num'] = df['nci_id'].str[4:8] + df['nci_id'].str[9:14]

    new_df = df.where(df['nci_id_num'] >= nci_id)
    new_df = new_df.dropna()

    return new_df


def get_new_trials(nci_id = get_latest_nci(14)):
    # Parameters: date, nci_id
    '''
    Returns a DataFrame containing information about all trials with record verificaiton dates on or after yesterday
    '''

    # SELECT VALUES TO INCLUDE IN DATAFRAME , ******EDIT THISSSS********
    #columns = ['record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
    #'completion_date', 'eligibility', 'brief_summary', 'detail_description', 'primary_purpose', 'intervention',
    #'sites', 'phase', 'nct_id']

    # if gene occurs in summary add it

    columns = ['record_verification_date', 'nci_id', 'official_title', 'lead_org', 'current_trial_status', 'start_date',
    'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id', 'eligibility', 'sites']

    data_df = pd.DataFrame(columns=columns)

    date = str(datetime.date.today() - datetime.timedelta(days=1))
    #date = '2021-10-30'

    # getting the total
    small_data = api_getter(date, '0', '1').json()
    total = small_data['total']
    #return small_data
    #return small_data['total']

    for i in range(0, total, 50) :
        full_data = api_getter(date, i, '50').json()
        #checks if api getter gets some kind of data

        print('Total trials:', total)
        print('Current Index:', i)
        print('Percent Completed', str(round(i / total * 100, 1)) + '%')
        print(full_data['total'])
        #print(full_data['data'])

        for trial in full_data['data']:
            #print(trial.items())
            data_df = data_df.append({key: str(value) for key, value in trial.items() if key in columns}, ignore_index=True)

    # Changes start_date to a date object, can do for other date coluns as well
    #data_df['start_date'] = [datetime.date.fromisoformat(date) for date in data_df['start_date']]

    return sorting_df(data_df, nci_id)

print(get_new_trials())
