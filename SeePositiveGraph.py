# -*- coding: utf-8 -*-
import wx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class SPGFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,wx.ID_ANY,'新型コロナウイルス新規感染者の推移',size=(600,400),style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

        #ルートパネル
        root_panel=wx.Panel(self,wx.ID_ANY)
        #ルートパネル内に設置するパネル
        button_panel=LeftPanel(root_panel)
        textbox_panel=RightPanel(root_panel)
        #ルートパネルレイアウト
        root_layout=wx.BoxSizer(wx.HORIZONTAL)
        root_layout.Add(button_panel,1,wx.TOP|wx.LEFT|wx.RIGHT,border=20)
        root_layout.Add(textbox_panel,1,wx.GROW|wx.ALL,border=20)
        root_panel.SetSizer(root_layout)


class LeftPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent,wx.ID_ANY)
        #ボタン
        update_button     =wx.Button(self,wx.ID_ANY,'データを更新',size=(200,50))
        showgraph_button  =wx.Button(self,wx.ID_ANY,'グラフを表示',size=(200,50))
        #ボタンのフォント変更
        font=wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        update_button.SetFont(font)
        showgraph_button.SetFont(font)
        #ボタンホバーメッセージ
        update_button.SetToolTip('CSVデータを取得し更新します．')
        showgraph_button.SetToolTip('CSVデータからグラフを作成し表示します．')
        #ボタンイベント
        update_button.Bind(wx.EVT_BUTTON,click_update_button)
        showgraph_button.Bind(wx.EVT_BUTTON,click_showgraph_button)
        #テキストラベル
        font=wx.Font(13,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        State_text=wx.StaticText(self,wx.ID_ANY,'グラフで表示する県')
        State_text.SetFont(font)
        global Sum_text
        Sum_text=wx.StaticText(self,wx.ID_ANY,'データが取得できませんでした．')
        try:
            data=pd.read_csv("COVID_Data.csv")
            Sum_text.SetLabel('データ数:{0}'.format(len(data[data["Prefecture"]=='ALL'])))
        except:
            pass
        #テキストをホバーした際に出すメッセージ
        State_text.SetToolTip('グラフで表示する県名')
        #コンボボックス
        element_array=('すべて','愛知県')
        global State_combobox
        State_combobox=wx.ComboBox(self,wx.ID_ANY,'選択してください',
                                         choices=element_array,style=wx.CB_READONLY)

        #BoxSizerの文字
        box=wx.StaticBox(self,wx.ID_ANY,'操作パネル')
        #ボタンレイアウト
        layout=wx.StaticBoxSizer(box,wx.VERTICAL)
        layout.Add(update_button,1,wx.CENTER|wx.TOP|wx.BOTTOM,border=15)
        layout.Add(showgraph_button,1,wx.CENTER|wx.TOP|wx.BOTTOM,border=15)
        layout.Add(State_text)
        layout.Add(State_combobox,1,wx.GROW)
        layout.Add(Sum_text,0,wx.BOTTOM)
        self.SetSizer(layout)

class RightPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent,wx.ID_ANY)
        #テキストボックス
        global min,max,interval
        min=wx.TextCtrl(self,wx.ID_ANY,'0')
        max=wx.TextCtrl(self,wx.ID_ANY,'0')
        interval=wx.TextCtrl(self,wx.ID_ANY,'7')
        font=wx.Font(17,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        min.SetFont(font)
        max.SetFont(font)
        interval.SetFont(font)
        #テキストラベル
        min_text=wx.StaticText(self,wx.ID_ANY,'開始')
        max_text=wx.StaticText(self,wx.ID_ANY,'終了')
        interval_text=wx.StaticText(self,wx.ID_ANY,'間隔')

        font2=wx.Font(13,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        min_text.SetFont(font2)
        max_text.SetFont(font2)
        interval_text.SetFont(font2)

        #テキストをホバーした際に出すメッセージ
        min_text.SetToolTip('グラフに使用する数値の最小値')
        max_text.SetToolTip('グラフに使用する数値の最大値')
        interval_text.SetToolTip('グラフの間隔')
        #BoxSizerの文字
        box=wx.StaticBox(self,wx.ID_ANY,'データ選択')
        #テキストボックスレイアウト
        layout=wx.StaticBoxSizer(box,wx.VERTICAL)
        layout.Add(min_text)
        layout.Add(min,1,wx.SHAPED|wx.RIGHT|wx.TOP|wx.BOTTOM,border=10)
        layout.Add(max_text)
        layout.Add(max,1,wx.SHAPED|wx.RIGHT|wx.TOP|wx.BOTTOM,border=10)
        layout.Add(interval_text)
        layout.Add(interval,1,wx.SHAPED|wx.RIGHT|wx.TOP|wx.BOTTOM,border=10)
        self.SetSizer(layout)

#イベント関連
#CSV更新
def click_update_button(event):
    url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
    try:
        data=pd.read_csv(url)
        pd.DataFrame(data).to_csv('COVID_Data.csv')
        wx.MessageBox('CSVファイルを更新しました．','メッセージ')
        Sum_text.SetLabel('データ数:{0}'.format(len(data[data["Prefecture"]=='ALL'])))
    except:
        wx.MessageBox(u'CSVファイルが取得できませんでした．', u'エラー', wx.ICON_ERROR)

#グラフ表示
def click_showgraph_button(event):
    try:
        data=pd.read_csv("COVID_Data.csv")
    except:
        wx.MessageBox(u'CSVファイルが存在しません．CSVファイルを更新してください．', u'エラー', wx.ICON_ERROR)
    print(State_combobox.GetStringSelection())
    if(State_combobox.GetStringSelection()==""):
        wx.MessageBox(u'県を選択してください．',u'エラー',wx.ICON_ERROR)
        return
    elif(State_combobox.GetStringSelection()=="すべて"):
        State='ALL'
    else:
        State=State_combobox.GetStringSelection()

    data=data[data["Prefecture"]==State]
    left=data['Date']
    height=data['Newly confirmed cases']
    flg=plt.figure(figsize=(10.0,8.0))
    ax=flg.add_subplot(111)
    plt.tight_layout()
    ax.set_position([0.1,0.15,0.8,0.8])
    plt.bar(left,height,width=1.0,edgecolor="black",linewidth=0.1,label="Positive")
    plt.xlabel('Date')
    plt.ylabel('Positive')
    plt.xticks(rotation=90)
    plt.xticks(np.arange(0,len(data),int(interval.GetValue())))
    plt.grid(b=True,axis='y',color='#666666',linestyle='-')
    plt.show()
#url='C:\\User

if __name__ == '__main__':
    app=wx.App()
    frame=SPGFrame()
    frame.Show()
    app.MainLoop()

"""
def showgraph(start_day,end_day,interval):
    data=getCSV().loc[int(start_day):int(end_day)]
    df = pd.DataFrame(data)
    left = df['Date']
    height = df['Newly confirmed cases']
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
"""
