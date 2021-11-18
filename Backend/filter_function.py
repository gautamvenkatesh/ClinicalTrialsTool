import requests
import json
from datetime import datetime

from requests import api 

#For now, we are just going to implement the “general search” which means to search by a query string
# Should be able to search, filter, sort
# Search string
# Sort by start date, end date, relevance (default output)
# Filter by genes (specific genes, or just any gene) #2 
# Status and Phase filters #3 drop down 
# Company blacklist #1 
# Keep in mind the UI will be paginated - we don’t need to get ALL of the clinical trials for a search
# Information should be the same as the one for the cron job, reference the spec above for those fields

# search_string, sort type, gene string,  phase, status

# database = None
with open('test_data.json', 'r') as content:
    data = json.load(content)['data']

new_string = json.dumps(data, indent=2)

#Converts date structure of year-month-day to datetime object 
def convert_dateString_to_dateTime(date): 
    
    return datetime.fromisoformat(date)


# Returns a list of trials that has been sorted

# INCLUDE_PARAMETERS = ['total', 'record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
#                 'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id', 'eligibility', 'sites']

INCLUDE_PARAMETERS = ['total', 'record_verification_date', 'nci_id', 'lead_org', 'official_title', 'current_trial_status', 'start_date',
                'completion_date', 'brief_summary', 'detail_description', 'primary_purpose', 'phase', 'nct_id']



def filter_data(search_string=None, sort_type=None, status_filter=[], phase_filter=[], company_blacklist=[]):
    
    # search_string = search_string.lower() if search_string else None
    api_base_url = 'https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&'
    # 50 is the limit
    headers= {'x-api-key': 'T0GzvGRulK6fFeFVzjmeo1Est2KbWeW25OXpyszf'}
    #API doesnt have sorting nor blacklist fields
    if sort_type == 'nci_id':
        api_base_url = api_base_url + 'sort=' + sort_type + '&'
    if search_string:
        api_base_url = api_base_url + 'keyword=' + search_string + '&'
    for status in status_filter: 
        api_base_url = api_base_url + 'trial_status=' + status + '&'
    for phase in phase_filter:
        api_base_url = api_base_url + 'phase=' + phase + '&'
    for param in INCLUDE_PARAMETERS: 
        api_base_url = api_base_url + 'include=' + param + '&'


    r = requests.get(api_base_url, headers= headers).json()['data']
    filteredData = list(filter(lambda trial: trial['lead_org'].lower() not in company_blacklist , r))

    if sort_type == 'start_date':
        filteredData.sort(key = lambda trial: convert_dateString_to_dateTime(trial['start_date']).strftime('%s'))
    return filteredData






