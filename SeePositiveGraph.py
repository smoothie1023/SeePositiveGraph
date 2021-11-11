# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
import tkinter as tk
from tkinter import messagebox
import os

url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'

def showgraph(start_day,end_day,interval):
    data=getCSV().loc[int(start_day):int(end_day)]
    df = pd.DataFrame(data)
    left = df['日付']
    height = df['PCR 検査陽性者数(単日)']
    fig = plt.figure(figsize=(10.0, 8.0))
    ax = fig.add_subplot(111)
    plt.tight_layout()
    ax.set_position([0.1,0.15,0.8,0.8])
    plt.bar(left,height,width=1.0,edgecolor="black",linewidth=0.1,label="Positive")
    plt.xlabel('date')
    plt.ylabel('Positive')
    plt.xticks(rotation=90)
    plt.xticks(np.arange(0, len(df), int(interval)))
    plt.grid(b=True, axis='y', color='#666666', linestyle='-')
    plt.show()

def reloadgraph():
    if min.get()>max.get():
        messagebox.showwarning("エラー", "開始の値は終了の値より小さい必要があります")
        return
    plt.close()
    try:
        showgraph(min.get(),int(max.get())-1,interval.get())
    except ValueError:
        messagebox.showwarning("不正な値","数値を入力してください")



def getCSV():
    try:
        data = pd.read_csv('COVID_Data.csv')
    except FileNotFoundError:
        try:
            data = pd.read_csv(url)
            pd.DataFrame(data).to_csv('COVID_Data.csv')
        except:
            print("Error:Something wrong with network or URL.")
            sys.exit()
    return data

def reloadCSV():
    data=pd.read_csv(url)
    pd.DataFrame(data).to_csv('COVID_DATA.csv')


def on_closing():
    plt.gca().clear()
    root.destroy()
    sys.exit()

root=tk.Tk()

root.title('操作パネル')
root.geometry('400x200')


####################################################################
csv_reload = tk.Button(root,text='csvを更新する',command= reloadCSV)
graph_button = tk.Button(root,text='グラフ表示＆更新',command=lambda:reloadgraph())

min=tk.Entry(root,width=20)
max=tk.Entry(root,width=20)
interval=tk.Entry(root,width=20)

min.insert(tk.END,"0")
max.insert(tk.END,str(len(pd.DataFrame(getCSV()))))
interval.insert(tk.END,"7")

minlabel=tk.Label(text="開始")
maxlabel=tk.Label(text="終了")
intervallabel=tk.Label(text="間隔")
maxvalue=tk.Label(text="データ数:"+str(len(pd.DataFrame(getCSV()))))
###################################
csv_reload.place(x=30,y=30)
graph_button.place(x=30,y=90)

min.place(x=150,y=30)
max.place(x=150,y=90)

interval.place(x=150,y=150)
minlabel.place(x=150,y=9)
maxlabel.place(x=150,y=69)
intervallabel.place(x=150,y=129)
maxvalue.place(x=30,y=150)
#####################################


root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
