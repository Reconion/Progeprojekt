import requests
import pickle
import json
import urllib
import os
os.chdir("/home/pi/Desktop/Progeprojekt")
##pip install requests
##pip install schedule

##Get token and save to pickle
def refresh_token():
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

##Save item data
##def get_data():
##    data = json.loads(get_dump())
##    url = data["files"][0]["url"]
##    lastModified = data["files"][0]["lastModified"]
##    ##write auction data json file
##    with open(str(lastModified) + ".json", "w") as f:
##        aucdata = requests.get(url)
##        
##        f.write(aucdata.text)
##            

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
##            vajalik esialgse itemID ja itemname library jaoks
def write_items():  
    with open("1540813527000.json") as f:
        data = json.loads(f.read())
        items = {}
        for i in range(len(data["auctions"])):
##        for i in range(5):
            itemID = data["auctions"][i]["item"]
            if itemID not in items:
                itemname = json.loads(get_itemname(itemID))["name"]
                print(str(i) + ".   " + str(itemID) + " - " + itemname)
                items[itemID] = itemname 
            else:
                continue
    with open("items.json", "w") as f:
        json.dump(items, f)
        
        
def add_item(item, i=""):
    with open("items.json") as f:
        data = json.load(f)
    data[item] = json.loads(get_itemname(item))["name"]
    print(str(i) + ". Added " + data[item] + " to library (" + str(item) +")")
    with open("items.json", "w") as f:
        json.dump(data, f)
    return data[item]
def get_data():
    data = json.loads(get_dump())
    url = data["files"][0]["url"]
    lastModified = data["files"][0]["lastModified"]
    ##write auction data json file
    print("Getng the data, this might take a while")
    aucdata = json.loads(requests.get(url).text)
    print("Processing")
    auctions = {}
    with open("items.json") as f:
        itemnames = json.load(f)
    for i in range(len(aucdata["auctions"])):
        auc_item = aucdata["auctions"][i]["item"]
        if str(auc_item) not in itemnames:
            itemnames[str(auc_item)] = add_item(str(auc_item), i)
        if itemnames[str(auc_item)].upper() not in auctions:
            auctions[itemnames[str(auc_item)].upper()] = {}
            auctions[itemnames[str(auc_item)].upper()]["buyouts"] = []
            auctions[itemnames[str(auc_item)].upper()]["buyouts"].append(int(aucdata["auctions"][i]["buyout"]/aucdata["auctions"][i]["quantity"]))
            auctions[itemnames[str(auc_item)].upper()]["quantity"] = aucdata["auctions"][i]["quantity"]
            
        else:
            auctions[itemnames[str(auc_item)].upper()]["buyouts"].append(int(aucdata["auctions"][i]["buyout"])/aucdata["auctions"][i]["quantity"])
            auctions[itemnames[str(auc_item)].upper()]["quantity"] += aucdata["auctions"][i]["quantity"]
        if int(aucdata["auctions"][i]["buyout"]) == 0:
            auctions[itemnames[str(auc_item)].upper()]["buyouts"].remove(0)
            auctions[itemnames[str(auc_item)].upper()]["quantity"] -= aucdata["auctions"][i]["quantity"]
    ##Process auctions
    for i in auctions:
        if auctions[i]["quantity"] != 0:
            auctions[i]["avg_buyout"] = int(sum(auctions[i]["buyouts"])/len(auctions[i]["buyouts"]))
            auctions[i]["min_buyout"] = min(auctions[i]["buyouts"])
        auctions[i].pop("buyouts")
    ##Write to json
    with open("data/" + str(lastModified) + ".json", "w") as f:
        json.dump(auctions, f)
##Tuleb raspberry schedule hoopis
####Jookse raspberry peal
##schedule.every().day.at("00:00").do(get_data)
##schedule.every().day.at("03:00").do(get_data)
##schedule.every().day.at("06:00").do(get_data)
##schedule.every().day.at("09:00").do(get_data)
##schedule.every().day.at("12:00").do(get_data)
##schedule.every().day.at("15:00").do(get_data)
##schedule.every().day.at("18:00").do(get_data)
##schedule.every().day.at("21:00").do(get_data)
##while 1:
##    schedule.run_pending()
##    time.sleep(1)
##Clearing schedule (programmi seisma jätmine ei clreari eelmisi schedule asju)
##schedule.clear()
get_data()
