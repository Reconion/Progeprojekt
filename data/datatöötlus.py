def use_data(find_name):
    import os
    import json
    import time
    find_name = find_name.upper()
    loetelu = []
    aeg = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".json"):
            aeg.append(time.ctime(float(filename.strip(".json")[:-3]+".000")))
            with open(filename, "r") as f:
                data = json.load(f)
            loetelu.append(data[find_name])
    return loetelu,aeg


def draw_data(asjad, ajad):
    import plotly.plotly as py
    import plotly.graph_objs as go
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
    py.plot(data, filename= "line-mode")
    
    
suvaline_asi = use_data(input("Mis itemi hinda tahad: ")) 
draw_data(suvaline_asi[0],suvaline_asi[1])

    
    