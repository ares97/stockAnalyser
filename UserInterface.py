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

import urllib
import json

import pandas as pd
import numpy as np

style.use("dark_background")

LARGE_FONT = ("Verdana", 12)

f = Figure(figsize=(5, 5), dpi=100)
graph = f.add_subplot(111)


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def generateChart(stock):
    graph.clear()
    stockPriceUrl = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=6m/csv'

    sourceCode = urllib.request.urlopen(stockPriceUrl).read().decode()

    stockData = []
    splitSource = sourceCode.split('\n')

    for line in splitSource:
        splitLine = line.split(',')
        if len(splitLine) == 6:
            if 'values' not in line and 'labels' not in line:
                stockData.append(line)

    date, closePrice, highPrice, lowPrice, openPrice, volume = np.loadtxt(stockData, delimiter=',', unpack=True,
                                                                          converters={0: bytespdate2num('%Y%m%d')})
    graph.plot_date(date, closePrice, '')


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
        label = tk.Label(self, text="Pick graph stock exchange", font="LARGE_FONT")
        label.pack(pady=10, padx=10)

        stockEntry = tk.Entry(self)
        stockEntry.pack()

        button = tk.Button(self, text="next",
                           command=lambda: prepChart())
        button.pack()

        def prepChart():
            generateChart(stockEntry.get())
            controller.show_frame(StartPage2)


class StartPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph page", font="LARGE_FONT")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="back to home page",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar.update()


app = StockAnalyser()
app.mainloop()
