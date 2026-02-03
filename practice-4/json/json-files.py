import json

with open("practice-4/json/sample-data.json", "r") as file:
    data = json.load(file)
    print(f"JSON raw data: {data}")
    print(f"Company: {data['company']}")
    print(f"Headquarters' address: {data['headquarters']['address']}")
    print("Employee:", data['employees'][0]['name'])
    print("Employee's contact email:", data['employees'][0]['contact']['email'])
    print("Project:", data['projects'][0]['name'])
    print("Project's budget:", data['projects'][1]['budget'])