import json

with open("1540813527000.json", "r") as read_file:
    data = json.load(read_file)

vajalikud = {}
for i in data["auctions"]:
    vajalikud[i["auc"]] = ([i["item"]],[i["bid"]], [i["quantity"]])
    
f = open("vajalik.txt", "w+")

f.write(str(vajalikud))
f.close


    
    