def use_data(find_name):
    import os
    import json
    import time
    
    find_name = find_name.upper()
    loetelu = []
    aeg = []
    for filename in os.listdir(os.getcwd()+"\\data"):
        if filename.endswith(".json"):
            aeg.append(time.ctime(float(filename.strip(".json")[:-3]+".000")))
            with open("data/"+filename, "r") as f:
                data = json.load(f)
            loetelu.append(data[find_name])
    return loetelu,aeg,find_name



def draw_data(asjad, ajad, asi):
    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly
    py.sign_in("progeprojekt","KWqEAqvRK5APokKTNEwe")
    kogus = []
    keskmine_hind = []
    min_hind = []
    for i in asjad:
        kogus.append(i["quantity"])
        keskmine_hind.append(i["avg_buyout"])
        min_hind.append(i["min_buyout"])
        
    trace1 = go.Scatter(
        x = ajad,
        y = kogus,
        mode = "lines",
        name = "kogus")
    
    trace2 = go.Scatter(
        x = ajad,
        y = keskmine_hind,
        mode = "lines",
        name = "keskmine hind")
    
    trace3 = go.Scatter(
        x = ajad,
        y = min_hind,
        mode = "lines",
        name = "miinimumhind")
    
    data = [trace1,trace2,trace3]
    
    layout = go.Layout(
        title=asi,
        xaxis=dict(
            title="Kuupäev",
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f')),
        yaxis=dict(
            title="Hind",
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f')))
    
    return plotly.offline.plot({"data":data,"layout":layout},auto_open=True)
 
from tkinter import *
def show_entry_fields():
    try:
        graafik(e1.get())
        e1.delete(0,END)
    except:
        print("Sellist itemit ei ole!")
def update():
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
    
    
master = Tk()
Label(master, text="Item").grid(row=0)

e1 = Entry(master)
e1.insert(INSERT,"Sisesta eseme nimi")
e1.grid(row=0, column=1)

Button(master, text='Välju', command=master.destroy).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Update', command=update).grid(row=3, column=2, sticky=W, pady=4)
Button(master, text='Joonista', command=show_entry_fields).grid(row=3, column=1, sticky=N, pady=4)

def graafik(e1):
    suvaline_asi = use_data(e1) 
    draw_data(suvaline_asi[0],suvaline_asi[1],suvaline_asi[2])


mainloop( )