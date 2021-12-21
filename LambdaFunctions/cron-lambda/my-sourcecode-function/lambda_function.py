from pymongo import MongoClient
import requests
import json
import datetime
import pandas as pd
import re

#UTILS start
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
    if not brief_sum:
        brief_sum = ""
    if not descrip:
        descrip = ""
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
    if not brief_sum:
        brief_sum = ""
    if not descrip:
        descrip = ""
    found_strings = []
    if ("NGS" in brief_sum) or ("NGS" in descrip):
        found_strings.append("NGS")
    for word in FLAGGED_STRINGS:
        if (word in brief_sum.lower()) or (word in descrip.lower()):
            found_strings.append(word)
    return found_strings
#Utils End

#Cronjob Start
CONNECTION_STRING = "mongodb+srv://upsync:upsync@cluster0.p5teq.mongodb.net/test"

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

    new_df = df.where(df['nci_id'] > nci_id)
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
    date = datetime.datetime.today() - datetime.timedelta(days = 7)

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

def update_latest_nci_id(nci_id):

    client = MongoClient(CONNECTION_STRING)
    trials_db = client['burning_rock_db_v2']
    trials = trials_db['latest']
    trials.delete_many({})
    trials.insert_one({'nci_id': nci_id})

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

#Cronjob end

#Constants start
# should I account for capitalized flagged string words?
genes = ['EPHA7', 'ERCC2', 'CTNNB1', 'GID4', 'KDM5C', 'IFNGR1', 'CDKN2A', 'BCORL1', 'SOX9', 'ALOX12B', 'PDCD1LG2', 'H3F3C', 'ZBTB2', 'NTRK3',
           'CDK6', 'BCL2L1', 'MUTYH', 'DCUN1D1', 'AKT1', 'FGF19', 'NBN', 'CTNNA1', 'ERBB3', 'RAC1', 'BARD1', 'ERG', 'FYN', 'STK11', 'IRF4', 'PRKDC',
           'NUTM1', 'POLE', 'MAP3K1', 'KMT2C', 'PBRM1', 'FANCI', 'PARP2', 'HIST1H3C', 'SLIT2', 'CDKN2C', 'SMARCD1', 'RAD50', 'CIC', 'FLT3', 'GATA1',
           'CXCR4', 'ROS1', 'BBC3', 'HIST1H2BD', 'CYLD', 'CDKN1C', 'RNF43', 'BTG2', 'KAT6A', 'HDAC1', 'NCOR1', 'PPP6C', 'ZNF217', 'MYC',
           'BRCA2', 'MKNK1', 'NSD2', 'MLH1', 'NTRK1', 'NKX2-1', 'MYCL', 'ETV4', 'ERBB4', 'SPOP', 'TEK', 'GLI1', 'AXIN2', 'PLK2', 'WISP3', 'PTEN',
           'YAP1', 'CEBPA', 'GATA4', 'TNFRSF14', 'MLH3', 'VEGFB', 'ID3', 'SMO', 'RIT1', 'ATRX', 'TIPARP', 'TOP1', 'TRIM58', 'ARID1B', 'EPHA3', 'PTPRT',
           'SDHB', 'PAX5', 'CASP8', 'RHEB', 'FANCF', 'RUNX1T1', 'CENPA', 'ERRFI1', 'NSD3', 'AXIN1', 'EP300', 'NCOR2', 'EZH2', 'CTCF', 'SF3B1', 'FOXA1',
           'SDHAF2', 'FANCD2', 'SPEN', 'MST1', 'BRIP1', 'SHQ1', 'RET', 'GSK3B', 'TET2', 'CD274', 'SOX17', 'KMT2D', 'FLCN', 'PPARG', 'XRCC2', 'MYCN', 'NUP93',
           'DNMT3A', 'PIK3C2G', 'MALT1', 'ACVR1B', 'SETD2', 'PRKCI', 'PDCD1', 'ESR1', 'ERCC1', 'MAX', 'FBXW7', 'XIAP', 'FRS2', 'SMARCA4', 'QKI', 'FUBP1',
           'CHEK1', 'NAV3', 'CYP17A1', 'MEF2B', 'PGR', 'MTAP', 'H3F3A', 'NFKBIA', 'SUFU', 'STK40', 'PHOX2B', 'CDKN1A', 'NKX3-1', 'EGFR', 'ERCC4', 'SMAD2',
           'ERCC5', 'CDKN2B', 'PIK3R3', 'ZNRF3', 'PIK3CD', 'BCL6', 'PIM1', 'NTHL1', 'FGF12', 'HIST1H3I', 'IKZF1', 'HNF1A', 'FOXP1', 'KDM6A', 'HLA-B', 'PTPRS',
           'ZNF703', 'JUN', 'KDM5A', 'TSC1', 'SLX4', 'GRM3', 'EMSY', 'HDAC2', 'KLF4', 'PIK3CA', 'HOXB13', 'ACVR1', 'IKBKE', 'PCDH11X', 'U2AF1', 'TBX3', 'TERC',
           'HIST2H3D', 'PRKAR1A', 'TGFBR2', 'GNA13', 'IRS2', 'FGF23', 'ASXL2', 'PDK1', 'PAK5', 'PTPRO', 'PRKN', 'CDK8', 'HLA-C', 'TENT5C', 'NRAS', 'MDM4', 'RBM10',
           'RARA', 'DDR2', 'RAD51C', 'MRE11', 'MAP2K1', 'NRG1', 'AURKA', 'ARAF', 'BCL10', 'CRLF2', 'MAGI2', 'PTPN11', 'EIF1AX', 'PIK3R1', 'TCF3', 'AURKB', 'POLD1',
           'IGF1', 'ARFRP1', 'RPA1', 'STAT4', 'CYP2D6', 'UGT1A1', 'BCL2L11', 'AR', 'NOTCH4', 'RASA1', 'BRCA1', 'APC', 'FOXO1', 'CCND2', 'PIK3CB', 'MAF', 'NEGR1',
           'PAK3', 'FAS', 'MEN1', 'PRDM1', 'HIST3H3', 'BAP1', 'RHOA', 'ICOSLG', 'MSH6', 'BTG1', 'RPTOR', 'DNMT1', 'PPP2R1A', 'ARID5B', 'BMPR1A', 'ETV6', 'SDC4CD74',
           'MST1R', 'HIST1H3G', 'ABRAXAS1', 'CUL4A', 'MDC1', 'SDHC', 'GRIN2A', 'HIST1H1C', 'CHD2', 'ZBTB16', 'IGF2', 'PPM1D', 'STAG2', 'BIRC3', 'AMER1', 'NOTCH2',
           'TRAF2', 'GNAQ', 'FAT1', 'H3F3B', 'BCL2', 'DAXX', 'TP53', 'WT1', 'FLT1', 'KEL', 'VEGFA', 'SH2D1A', 'RICTOR', 'JAK1', 'DIS3', 'CDK12', 'FOXL2', 'EPHA5',
           'P2RY8', 'PIK3C2B', 'CDH18', 'FGF7', 'CHD1', 'PTCH1', 'NOTCH1', 'TCF7L2', 'FGF10', 'JAK2', 'TMEM127', 'BCL2L2', 'SMARCB1', 'BRAF', 'DOT1L', 'GATA3',
           'EPHA2', 'XRCC3', 'MSH3', 'MIR21', 'TSC2', 'VHL', 'NF1', 'TOP2A', 'HIST1H3E', 'TNFAIP3', 'ERCC3', 'RUNX1', 'PARP1', 'HRAS', 'RAD51B', 'CHD4', 'RAD52',
           'SDHD', 'DDR1', 'RAB35', 'MET', 'RAD21', 'SMAD3', 'FANCA', 'EZR', 'PIK3R2', 'CSMD3', 'HIST1H3A', 'SDHA', 'REL', 'SLC34A2', 'FANCM', 'MAP2K4', 'PIK3CG',
           'TMPRSS2', 'NT5C2', 'MED12', 'ERBB2', 'NPM1', 'CD79B', 'NCOA3', 'FGF3', 'SOX2', 'MDM2', 'GPS2', 'INHBA', 'BCOR', 'SDC4', 'FANCE', 'RPS6KB2', 'IL10',
           'RAD51', 'AXL', 'CSF3R', 'FANCL', 'AKT3', 'LYN', 'INPP4B', 'KIT', 'GABRA6', 'B2M', 'MGA', 'PAK1', 'ASXL1', 'INSR', 'ATR', 'PDGFRA', 'EPCAM', 'DNAJB1',
           'FGFR3', 'IRS1', 'PARP3', 'PDGFRB', 'MPL', 'RAF1', 'MITF', 'RAD54L', 'MCL1', 'MAPK1', 'FANCG', 'SNCAIP', 'CARD11', 'MSH2', 'FANCC', 'KEAP1', 'HGF',
           'TGFBR1', 'CBL', 'SOX10', 'TET1', 'BRINP3', 'DICER1', 'MTOR', 'CDC73', 'HIST1H3D', 'AKT2', 'MYD88', 'CDKN1B', 'FLT4', 'RAD51D', 'HSD3B1', 'KRAS',
           'LTK', 'TP63', 'DPYD', 'CHEK2', 'MERTK', 'FGF6', 'ARID1A', 'GATA6', 'CDK4', 'PLCG2', 'MAP3K13', 'CTLA4', 'BRD4', 'SRSF2', 'LATS1', 'CRKL', 'LATS2',
           'STAT3', 'ETV5', 'FGFR1', 'PALB2', 'CALR', 'LRP1B', 'SOCS1', 'TYRO3', 'SGK1', 'IDH1', 'SYK', 'FGFR2', 'STAT5B', 'ABL2', 'INPP4A', 'PIK3C3', 'SPTA1',
           'SRC', 'NSD1', 'IRF2', 'BLM', 'MAPK3', 'KMT2A', 'IDH2', 'KDR', 'TRAF7', 'CD79A', 'XPO1', 'PREX2', 'BTK', 'NOTCH3', 'CREBBP', 'CCND3', 'HIST1H3J', 'GEN1',
           'ATM', 'JAK3', 'ARID2', 'RSPO2', 'CUL3', 'RECQL4', 'GATA2', 'CD74', 'HLA-A', 'TAF1', 'DNMT3B', 'EPHB1', 'STAT5A', 'IGF1R', 'TERT', 'PNRC1', 'NF2', 'CBFB',
           'TSHR', 'GNAS', 'CDH1', 'SH2B3', 'PMS2', 'PPP2R2A', 'HIST1H3H', 'RB1', 'NTRK2', 'HIST1H3B', 'EWSR1', 'CCNE1', 'EIF4E', 'GNA11', 'PTPRD', 'CSMD1', 'ALK',
           'RPS6KA4', 'HSP90AA1', 'KLHL6', 'SMAD4', 'MYOD1', 'GREM1', 'IL7R', 'NFE2L2', 'PMS1', 'LMO1', 'TRPC5', 'CCND1', 'MAP2K2', 'FGF4', 'FGF14', 'YES1', 'FH',
           'EPHB4', 'WRN', 'FGFR4', 'EED', 'INHA', 'CSF1R']

FLAGGED_STRINGS = [
   "mutation",
   "mutations",
   "receptor",
   "pathway",
   "biomarker",
   "biomarkers",
   "gene",
   "genes",
   "solid tumor",
   "advanced solid tumors",
   "genetic alterations",
   "NGS",
   "sequencing"
]

#Constants end

#lambda_function start
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

def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps("New trials successfully retrieved.")
    }