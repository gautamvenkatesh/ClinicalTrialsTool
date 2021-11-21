import requests
import json
import datetime
import pandas as pd
import re
from constants import genes
from constants import FLAGGED_STRINGS

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
        url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?size=50&record_verification_date_gte=" + formatted_date + '&from=' + str(start_index)

        payload = {}
        headers = {
            'x-api-key': 'wucyqb6KsT94qFV7W8aog8XokfTjfIBKIQoA0hgj',
        }

        full_data = requests.request("GET", url, headers=headers, data=payload).json()

        if not full_data:
            break

        if start_index == 0:
            total = full_data['total']
        
        for trial in full_data['data']:
            nci = int(trial['nci_id'][4:8] + trial['nci_id'][9:])
            if nci > max_nci_id:
                max_nci_id = nci
        
        start_index += 50
    
    if max_nci_id == 0:
        return "There are no trials that have a record verification date from within the past " + str(num_prev_days) + " days. Please increase num_prev_days."
    #verify that max_nci_id is the greatest nci_id
    else:
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
        #return nci_id
        return "NCI-" + str(nci_id)[0:4] + "-" + str(nci_id)[4:]

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


#testing find_genes and find_strings
#print(find_genes("hi my name is. ERCC3, MED12, HLA-A-MCL1-LYN. (FLT4)", "I like world STAT3, EED. CSF1R. EED")) 
#EED is not found because of extra spaces surrounding it in genes.
#print(find_strings("hi mutations are solid tumor. I-pathway!", "Biomarker is .gene. !SEQUENCING! NGS!")) 


#testing get_latest_nci
#print(get_latest_nci(5))