import requests
import json
import datetime
import pandas as pd

def api_getter(date, start_index, nci_id):

    s_date = date.strftime("%Y-%m-%d")

    url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=20&record_verification_date_gte=" + s_date
    url += 'nct_id>' + nci_id + '&from=' + str(start_index)

    payload = {}
    headers = {
        'x-api-key': 'mbxhNtV14K6tiaQ5IUHt2m0wpaKrz9H2cMAz1nHg',
    }
    full_data = requests.request("GET", url, headers=headers, data=payload)

    return full_data

def get_new_trials(date, nci_id):
    '''
    Returns a DataFrame containing information about all trials with record verificaiton dates on or after yesterday
    '''



    # SELECT VALUES TO INCLUDE IN DATAFRAME , ******EDIT THISSSS********
    columns = ['nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
    'completion_date', 'eligibility', 'detail_description', 'primary_purpose', 'intervention',
    'sites', 'phase', 'genes', 'url']

    data_df = pd.DataFrame(columns=columns)

    start_index = 0

    while True:
        full_data = api_getter(date, start_index, nci_id).json()

        # checks if api getter gets some kind of data
        try:
            total = full_data['total']
        except:
            print('SERVER ERROR, NOT ALL TRIALS MAY BE INCLUDED')
            break

        print('Total trials:', total)
        print('Current Index:', start_index)
        print('Percent Completed', str(round(start_index / total * 100, 1)) + '%')
        print()
        start_index += 50


        for trial in full_data['data']:
            data_df = data_df.append({key: value for key, value in trial.items() if key in columns}, ignore_index=True)

        if start_index >= total:
            break

    # Changes start_date to a date object, can do for other date coluns as well
    data_df['start_date'] = [datetime.date.fromisoformat(date) for date in data_df['start_date']]

    data_df.sort_values('nci_id', ascending=False, inplace=True)
    data_df.index = [i for i in range(len(data_df))]

    return data_df

print(get_new_trials().sort_values('nci_id', ascending=False))