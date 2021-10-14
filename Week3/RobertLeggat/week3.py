import json
import sys

original_stdout = sys.stdout

file = open('descriptions.txt', 'w')
sys.stdout = file

def main():
    #put filepath of JSON below
    j = open('response.json')
    #turns JSON into dictionary
    data = json.load(j)
    print("size " + str(len(data["data"])))
    #iterates to through all clinical trials
    for i in data["data"]:
        print("Title: " + i["official_title"])
        print("Phase: " + i["phase"])
        print('Description:', i['detail_description'])
        print('\n\n\n\n\n\n\n')
    j.close()

if __name__ == '__main__':
    main()