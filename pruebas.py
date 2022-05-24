import json, urllib, requests

with open('config.json', 'r') as f:
    data = json.load(f)

key = data['API_map']
base_url = "http://www.mapquestapi.com/search/v2/search?"

url = base_url + urllib.parse.urlencode({'key':key, 'origin':"{'city': 'Madrid'}", 'units':'k', 'sort':'relevance'})

print(url)