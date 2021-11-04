import requests
import json
import datetime
import pandas as pd

# Checks the past specified number of days (num_prev_days) and finds the greatest nci id from those trials. Then verifies that the 
# max nci_id it found is truly the greatest by checking for a trial with an nci_id that is 1 greater than the one found. If it finds 
# a trial with nci_id equal to max_nci_id + 1, it verifies that new nci_id is the greatest until no more greater nci_ids are found. 
# Returns the greatest nci_id as a 9 digit int.

def get_latest_nci(num_prev_days):
    date_two_weeks_ago = datetime.date.today() - datetime.timedelta(days=num_prev_days)
    formatted_date = date_two_weeks_ago.strftime("%Y-%m-%d")

    start_index = 0
    total = 2**63 - 1
    max_nci_id = 0

    while start_index < total:
        #likely can replace lines 21 to 28 with Sally's api_getter() function
        url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&record_verification_date_gte=" + formatted_date + '&from=' + str(start_index)

        payload = {}
        headers = {
            'x-api-key': 'wucyqb6KsT94qFV7W8aog8XokfTjfIBKIQoA0hgj',
        }

        full_data = requests.request("GET", url, headers=headers, data=payload).json()

        if start_index == 0:
            total = full_data['total']
        
        for trial in full_data['data']:
            nci = int(trial['nci_id'][4:8] + trial['nci_id'][9:])
            if nci > max_nci_id:
                max_nci_id = nci
        
        start_index += 50
    
    #verify that max_nci_id is the greatest nci_id
    return verify_greatest_nci(max_nci_id)

def verify_greatest_nci(nci_id):
    nci_id_plus_one = nci_id + 1
    url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&nci_id=NCI-" + str(nci_id_plus_one)[0:4] + "-" + str(nci_id_plus_one)[4:]

    payload = {}
    headers = {
        'x-api-key': 'wucyqb6KsT94qFV7W8aog8XokfTjfIBKIQoA0hgj',
    }

    full_data = requests.request("GET", url, headers=headers, data=payload).json()

    total = full_data['total']

    if total > 0:
        return verify_greatest_nci(nci_id_plus_one)
    else:
        return nci_id

#testing get_latest_nci
# print(get_latest_nci(7))

# def export_data_to_es(dataframe):
    # making sure no null or blank values in dataframe
#    for column in dataframe:
#        dataframe[column] = dataframe[column].apply(safe_value)
#
#    df_iter = dataframe.iterrows()
#    for index, document in df_iter:
#        # yield info from each cell in each row of dataframe
#        yield {
#            
#        }
#    raise StopIteration

#def safe_value(field_val):
#    return field_val if not pd.isna(field_val) else "Other"

#running export_data_to_est and inputting returned dataframe from Sally's get_new_trials() method
#helpers.bulk(es_client, export_data_to_es(get_new_trials()))
