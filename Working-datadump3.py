import requests
import pickle
import json

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
##print(get_dump())
data = json.loads(get_dump())