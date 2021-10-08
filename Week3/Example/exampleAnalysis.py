import json

def main():
    #put filepath of JSON below
    j = open('Week3/Example/exampledata.json')
    #turns JSON into dictionary
    data = json.load(j)
    print("size " + str(len(data["data"])))
    #iterates to through all clinical trials
    for i in data["data"]:
        print("Title: " + i["official_title"])
        print("Phase: " + i["phase"])
        print("Leading organization: " + i["lead_org"])
        print("Current Trial Status Date: " + i["current_trial_status_date"])
        print()
    j.close()

if __name__ == '__main__':
    main()
