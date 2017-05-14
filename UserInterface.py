import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import *

style.use("dark_background")


LARGE_FONT = ("Verdana", 12)
NASDAQ = ["TSLA.US", "AAPL.US", "AMD.US", "NVDA.US"];
NYSEEuronextUS = ""
JapanExchangeGroup = ""
stockMarkets = {'NASDAQ OMX': NASDAQ,
                'NYSE Euronext(US)': NYSEEuronextUS,
                'Japan Exchange Group': JapanExchangeGroup}

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

def animate(i):
    pullData = open("sampleStockData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList,yList)

class StockAnalyser(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        tk.Tk.wm_title(self, "Stock Analyser")
        tk.Tk.minsize(self, width=350, height=200)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, StartPage2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Pick a stock exchange", font="LARGE_FONT")
        label.pack(pady=10, padx=10)

        global stockExchangeList;
        stockExchangeList = tk.Listbox(self, height=5)
        stockExchangeList.pack()
        for item in stockMarkets:
            stockExchangeList.insert(END, item)
        button1 = tk.Button(self, text="next",
                            command=lambda: controller.show_frame(StartPage2))
        button1.pack()


class StartPage2(tk.Frame):
    shares = NONE

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph page", font="LARGE_FONT")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="back to home page",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas,self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar.update()



app = StockAnalyser()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
