import json

def main():
    json_data = open('./data.json')
    data = json.load(json_data)
    print("size " + str(len(data["data"])))
    for i in data["data"]:
        print("Title: " + i["official_title"])
        print("Phase: " + i["phase"])
        print("Leading organization: " + i["lead_org"])
        print("Current Trial Status Date: " + i["current_trial_status_date"])
        print("Current Trial Status: " + i["current_trial_status"])
        print("Primary purpose: " + i["primary_purpose"])
        print()
    json_data.close()

if __name__ == '__main__':
    main()