import requests
import json
import datetime
import pandas as pd

today = datetime.date.today()
# make method to start at previous date
url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&record_verification_date_gte=" + str(today)
url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&record_verification_date_gte=" + '2021-09-01'

payload = {}
headers = {
  'x-api-key': 'mbxhNtV14K6tiaQ5IUHt2m0wpaKrz9H2cMAz1nHg',
}

full_data = requests.request("GET", url, headers=headers, data=payload).json()
print("size " + str(len(full_data['data'])))
#iterates to through all clinical trials

# used to find list of keys, not needed in final product
keys = []
for trial in full_data['data']:
  keys.extend(list(trial.keys()))
keys = list(sorted(set(keys)))
print(keys)

# need to change column names because not all below are accurate
columns = ['nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
'completion_date', 'eligibility', 'detail_description', 'primary_purpose', 'intervention', 
'sites', 'phase', 'genes', 'url']

data_df = pd.DataFrame(columns=columns)
for trial in full_data['data']:
  data_df = data_df.append({key: value for key, value in trial.items() if key in columns}, ignore_index=True)

# Changes start_date to a date object, can do for other date coluns as well
data_df['start_date'] = [datetime.date.fromisoformat(date) for date in data_df['start_date']]

# filtering by start date
#print(data_df[data_df['start_date'] >= datetime.date(2017, 1, 1)])