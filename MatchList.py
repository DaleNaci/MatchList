import json
import urllib.request

url = "https://api.vexdb.io/v1/get_matches?team=750E&season=Turning%20Point&sku=RE-VRC-19-7004"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(data)
