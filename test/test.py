import urllib.request, json
from datetime import datetime

# with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/random.php") as url:
#     cockDict = json.loads(url.read().decode())
#     print(json.dumps(cockDict, indent=4, sort_keys=True))
# print(type(cockDict))
# #print(cockDict['drinks'])

tiem = datetime.now()
print(tiem.day)
