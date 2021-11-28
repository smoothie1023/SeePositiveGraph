# coding: utf-8
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as nps
import urllib.request
from io import StringIO
import numpy as np
State="ALL"
url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
data=pd.read_csv(url)

#print(dataReader['testedPositive',dataReader['prefectureNameJ']==city])
data=data[data["Prefecture"]==State]
print(data)
"""
for data in df:
    print(data)
"""

start=0
end=32207
interval=7

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
plt.xticks(np.arange(0,len(data),int(interval)))
plt.grid(b=True,axis='y',color='#666666',linestyle='-')
plt.show()
#url='C:\\Users\\smoothie\\Downloads\\covid19-master\\data\\prefectures.csv'
#url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
"""
def read_csv(url):
    res=urllib.request.urlopen(url)
    res=res.read().decode('utf-8')
    df=pd.read_csv(StringIO(res))
    return df
"""
"""
#response = urllib.urlopen(url)
#f = csv.reader(response)
#f=open(url,'r',encoding="utf-8")
dataReader = pd.read_csv(url,encoding="utf8")
#print(data.columns)

#data_col=data.columns



#dataReader=read_csv(url)
plot_x=[]
plot_y=[]
yesterday=0
city="愛知県"
#print(dataReader['testedPositive',dataReader['prefectureNameJ']==city])
#dataReader=dataReader[dataReader['prefectureNameJ']==city]

for row in dataReader:
    print(dataReader['year'])
    if(row[3]==city):
        plot_x.append(row[0]+"/"+row[1]+"/"+row[2])
        #plot_x.append(row[2])
        today=int(row[5])
        summary=today-yesterday
        if(summary<0):
            summary=0

        plot_y.append(summary)
        yesterday=int(row[5])


    print(row)
    if(row[3]=="愛知県"):
        print(row[0]+"/"+row[1]+"/"+row[2])
        print("positive"+row[5])


fig = plt.figure(figsize=(6.0, 4.0))
ax = fig.add_subplot(111)
plt.grid(b=True, axis='y', color='#666666', linestyle='-')
plt.xticks(rotation=90)
plt.xticks(np.arange(0, len(dataReader), 7))


plt.bar(plot_x,plot_y,width=1,label=city)
plt.show()

#plt.plot(dataReader['date'],dataReader['testedPositive'])
#plt.show()
#f.close()
"""
