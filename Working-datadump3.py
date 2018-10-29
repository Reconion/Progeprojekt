import requests
import pickle
import json
import urllib

##Get token and save to pickle
def refresh_token():
    import requests
    data = {
      'grant_type': 'client_credentials'
    }
    response = requests.post('https://eu.battle.net/oauth/token', data=data, auth=('d43b6412d0f14970823e61edecbccf6b', 'rRqnLdSMydx5TOeEsJAJccnTFmGFOLVp'))
    token = response.json()["access_token"]
    pickle.dump(token, open("token.p", "wb"))
##Read token from pickle
def get_token():
    try:
        return pickle.load(open("token.p", "rb"))
    except:
        refresh_token()

##Get auction data json
def get_dump():
    while True:
        try:
            token = get_token()
            headers = {
                'Authorization': 'Bearer ' + token,
            }
            params = (
                (':realm', 'tarren mill'),
                ('locale', 'en_GB')
            )
            response = requests.get('https://eu.api.blizzard.com/wow/auction/data/tarren mill', headers=headers, params=params)
            if response.text == "":
                refresh_token()
                print("Refreshing token")
            else:
                return(response.text)
                break
        except:
            print("proovin uuesti")
####get auction data
##data = json.loads(get_dump())
##url = data["files"][0]["url"]
##lastModified = data["files"][0]["lastModified"]
####write auction data json file
##with open(str(lastModified) + ".json", "w") as f:
##    aucdata = requests.get(url)
##    f.write(aucdata.text)
            

def get_itemname(itemID):
    while True:
        try:
            token = get_token()
            headers = {
                'Authorization': 'Bearer ' + token,
            }
            params = (
                (':itemId', itemID),
                ('locale', 'en_GB')
            )
            response = requests.get('https://eu.api.blizzard.com/wow/item/' + str(itemID), headers=headers, params=params)
            if response.text == "":
                refresh_token()
                print("Refreshing token")
            else:
                return(response.text)
                break
        except:
            print("proovin uuesti")
            
with open("1540813527000.json") as f:
    data = json.loads(f.read())
    for i in range(len(data["auctions"])):
        itemID = data["auctions"][i]["item"]
        itemname = json.loads(get_itemname(itemID))["name"]
        print(str(itemID) + " - " + itemname)
        
            