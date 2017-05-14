import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import *

LARGE_FONT = ("Verdana", 12)
NASDAQ = ["TSLA.US", "AAPL.US", "AMD.US", "NVDA.US"];
NYSEEuronextUS = ""
JapanExchangeGroup = ""
stockMarkets = {'NASDAQ OMX': NASDAQ,
                'NYSE Euronext(US)': NYSEEuronextUS,
                'Japan Exchange Group': JapanExchangeGroup}


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

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=TRUE)

        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=TRUE)


app = StockAnalyser()
app.mainloop()
