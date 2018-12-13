from bs4 import BeautifulSoup
import requests
import os
import re
import requests
import json
url = 'http://reconion.hopto.org/data/'
ext = 'json'

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

for file in listFD(url, ext):
    filename = re.search("(?<=data\/\/)(.*)(?=)" , file).group()
    if not os.path.isfile("./data/" + filename):
        aucdata = json.loads(requests.get(file).text)
        with open("data/" + filename, "w") as f:
            json.dump(aucdata, f)
