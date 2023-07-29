import requests
from datetime import datetime
from keys import airtable_token
import json

baseId = "appLJmbxQUcA617uZ"
tableId = "tbl8LUOvtbbPXwWHk"
headers = {
        "Authorization": "Bearer " + airtable_token,
}
url = "https://api.airtable.com/v0/" + baseId + "/" + tableId    

def get_birthday():
    current_month = datetime.now().month
    current_day = datetime.now().day
    # param = "filterByFormula=" + str(current_month) + "%3C%3D%7Bbirthday_month%7D%3C%3D" +  str(current_month + 1)
    response = requests.get(url, headers=headers)

    try:
        records = json.loads(response.text)["records"]
    except:
        print("Error getting birthdays")
        
    useful_records = []

    for record in records:
        fields = record["fields"]
        if int(fields["birthday_month"]) == current_month and int(fields["birthday_day"]) == current_day:
            useful_records.append([fields['name'], 'today'])
            break
        try:
            if int(fields["birthday_month"]) == current_month + 1 and int(fields["birthday_day"]) == current_day + 3 and fields["postcard"]:
                useful_records.append([fields['name'], 'next month so write a postcard'])
        except (KeyError):
            break
    return useful_records

def add_birthday(name, birthday):
    data = {
        "fields": {
            "name": name,
            "birthday_month": birthday.month,
            "birthday_day": birthday.day
        }
    }
    try:
        print(data)
        print(url)
        print(headers)
        response = requests.post(url=url, headers=headers, json=data)
        print(response.text)
    except:
        print("Error sending birthdays")


#print(add_birthday("Hello", "11/11"))