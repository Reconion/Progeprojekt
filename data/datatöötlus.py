
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
    return loetelu,aeg,find_name


def draw_data(asjad, ajad, asi):
    kogus = []
    keskmine_hind = []
    min_hind = []
    for i in asjad:
        kogus.append(i["quantity"])
        keskmine_hind.append(i["avg_buyout"])
        min_hind.append(i["min_buyout"])
        
    
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('TkAgg')
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    def clear():
        canvas.get_tk_widget().destroy()
        canvas.get_tk_widget().delete("all")


    class mclass:
        
        def __init__(self,  window):
            self.window = window
            self.box = Entry(window)
            self.button = Button (window, text="Item", command=self.plot)
        
            self.box.pack ()
            self.button.pack()

        def plot (self):
            try:
                clear()
            except:
                print("k´jou")
            x=np.array (ajad)
            v= np.array (kogus)
            p= np.array (keskmine_hind)
            k= np.array (min_hind)

            fig = Figure(figsize=(6,6))
            a = fig.add_subplot(111)
            a.plot(x,v,color='red',label="kogus")
            a.plot(x,p,color='blue',label="keskmine hind")
            a.plot(x,k,color="green",label="väikseim hind")

            a.set_title (asi, fontsize=16)
            a.set_ylabel("Hinnad", fontsize=14)
            a.set_xlabel("Aeg", fontsize=14)
            

            canvas = FigureCanvasTkAgg(fig, master=self.window)
            canvas.get_tk_widget().pack()
            canvas.draw()
            
 

    window= Tk()
    start= mclass (window)
    window.mainloop()
        
    
from tkinter import *
#def show_entry_fields():
#
#    graafik(e1.get())
#    e1.delete(0,END)
#
#master = Tk()
#Label(master, text="Item").grid(row=0)
#
#e1 = Entry(master)
#e1.insert(INSERT,"Sisesta eseme nimi")
#e1.grid(row=0, column=1)
#
#Button(master, text='Välju', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
#Button(master, text='Joonista', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

#def graafik(e1):
suvaline_asi = use_data("gloom dust") 
draw_data(suvaline_asi[0],suvaline_asi[1],suvaline_asi[2])


#mainloop( )
