import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates

import tkinter as tk
from tkinter import *
from tkinter import messagebox

import urllib
import json

import pandas as pd
import numpy as np

style.use("dark_background")

LARGE_FONT = ("Verdana", 12)

figure = Figure(figsize=(9, 5), dpi=75)
graph = figure.add_subplot(111)
stockData = []
currentStock = ""
boolStartRefreshingData = False
timeRange = 12


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def generateChart():
    graph.clear()
    stockData.clear()
    graph.set_xlabel('DATE')
    graph.set_ylabel('close price ($)')
    graph.set_title(currentStock)
    try:
        stockPriceUrl = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + currentStock + '/chartdata;type=quote;range=' + timeRange + 'm/csv'

        sourceCode = urllib.request.urlopen(stockPriceUrl).read().decode()

        splitSource = sourceCode.split('\n')

        for line in splitSource:
            splitLine = line.split(',')
            if len(splitLine) == 6:
                if 'values' not in line and 'labels' not in line:
                    stockData.append(line)

        date, closePrice, highPrice, lowPrice, openPrice, volume = np.loadtxt(stockData, delimiter=',', unpack=True,
                                                                              converters={0: bytespdate2num('%Y%m%d')})
        graph.plot_date(date, closePrice, '')
    except :
        warr = messagebox.showwarning("BE CAREFUL, COWBOY!", "There is no such stock or wrong time range")



    global boolStartRefreshingData
    boolStartRefreshingData = False


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
        label = tk.Label(self, text="write stock name(i.e TSLA,AAPL,NVDA)", font="LARGE_FONT")
        label.pack(pady=10, padx=10)

        stockEntry = tk.Entry(self)
        stockEntry.insert(END, 'PKO')
        stockEntry.pack()

        label2 = tk.Label(self, text="write time range in months", font="LARGE_FONT")
        label2.pack(pady=10, padx=10)

        timerangeEntry = tk.Entry(self)
        timerangeEntry.insert(END, '12')
        timerangeEntry.pack()

        button = tk.Button(self, text="next",
                           command=lambda: prepChart())
        button.pack()

        def prepChart():
            global currentStock, timeRange, boolStartRefreshingData
            timeRange = timerangeEntry.get()
            currentStock = stockEntry.get()
            boolStartRefreshingData = True
            controller.show_frame(StartPage2)


class StartPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button = tk.Button(self, text="back to choosing page",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar.update()


def animate(self):
    if boolStartRefreshingData == True:
        generateChart()


app = StockAnalyser()
ani = animation.FuncAnimation(figure, animate, 1)
app.mainloop()
