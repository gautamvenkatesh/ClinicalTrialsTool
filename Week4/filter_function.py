import requests
import json
from datetime import datetime 

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
#TODO: Debug actual request call (requests library is ONLY returning html script of API page instead of json data)
#TODO: End_date sorting 
#TODO: Gene filter (Doesnt seem to be gene attributes in json data)
def filter_data(search_string=None, sort_type='relevance', gene_filter=None, status_filter=None, phase_filter=None, company_blacklist=[]):
    search_string = search_string.lower() if search_string else None

    filteredStatusData = list(filter(lambda trial: trial['current_trial_status'] == status_filter if status_filter else True, data))
    # filteredStatusData = filter(lambda trial: trial['gene'] == gene_filter if not gene_filter else True, filteredStatusData)
    filteredStatusData = list(filter(lambda trial: search_string in trial['official_title'].lower() if search_string else True, filteredStatusData))
    filteredStatusData = list(filter(lambda trial: trial['phase'] == phase_filter if phase_filter else True, filteredStatusData))
    
    filteredStatusData = list(filter(lambda trial: trial['lead_org'].lower() not in company_blacklist , filteredStatusData))
    
    if sort_type == 'start_date': 
        filteredStatusData.sort(key = lambda trial: convert_dateString_to_dateTime(trial['start_date']).strftime('%s'))
    


    return filteredStatusData
print([ trial['start_date'] for trial in filter_data(sort_type = 'start_date', search_string='cancer')])
