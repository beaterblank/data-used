#import statements
import asciigraphics as a
a.createcanvas(100,50,False)
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os 
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates


timestamp = time.strftime('%d-%m-%Y,%H:%M:%S')
tss = timestamp.split(",")
ts=pd.to_datetime(tss[0],dayfirst=True)
options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(options=options)
driver.get('https://fuptopup.bsnl.co.in/manualRedirection.do');
btn = driver.find_element_by_id('btnKnowUsages')
btn.click()
finding =  True
while (finding):
    try:
        dat =  driver.find_element_by_xpath('//*[@id="jqg3"]/td[4]')
    except :
        continue
    finding=False
dataused = dat.get_attribute('title')
dataused = dataused.replace(' GB','')
dataused = dataused+','+timestamp
a.text(1,1,dataused,[15,15])
import os 
this_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(this_dir, 'data.csv')
with open(file_path,'a') as fd:
    fd.write(f'\n{dataused}')
if(ts.day==1):
    with open(file_path,'w') as fa:
        fa.write(f'Data,Date,Time\n0,1-05-2021,00:00:00\n{dataused}')
driver.close()


plt.style.use('seaborn')
this_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(this_dir, 'data.csv')
data = pd.read_csv(file_path)
data['Date'] = pd.to_datetime(data['Date'],dayfirst=True)
data.sort_values('Date', inplace=True)
diffa= float(data["Data"][len(data["Data"])-1])-float(data["Data"][0])
k = str(data["Date"][len(data["Date"])-1]).split("-")
l = str(data["Date"][0]).split("-")
k[-1]=k[-1].split(" ")
l[-1]=l[-1].split(" ")
k[-1][0]=int(k[-1][0])
l[-1][0]=int(l[-1][0])
diffb=k[-1][0]-l[-1][0]+1
expecteddate =str(round((diffa/diffb),2)) 
a.text(1,3,expecteddate+"GB/day :current rate of data usage",[10,10],False)
daysleft = (650-float(data["Data"][len(data["Data"])-1]))/float(expecteddate)
a.text(1,5,str(round(daysleft,2))+" days left at current rate of datausage",[0,1],False)
date = data['Date']
close = data['Data']
d_lis = []
c_lis = []
for i in date: 
    d_lis.append(int(i.day))
for i in close:
    c_lis.append(int(i))
a.text(7,9,"^data used(0-650)",[2,2],False)
a.text(83,43,">day(0-31)",[2,2],False)
a.line_2d(7,10,7,45,[5,5],5,False)
a.line_2d(2,43,82,43,[5,5],5,False)
y_cr = []
x_cr =[]
for i  in c_lis:
    y = 7+(1-i/650)*35
    y_cr.append(y)
for i in d_lis:
    x = 5+(i/31)*80
    x_cr.append(x)
for i in range(len(x_cr)):
    if(i<len(x_cr)-1):
        a.line_2d(x_cr[i],y_cr[i],x_cr[i+1],y_cr[i+1],[3,3],0,False)
    a.point(x_cr[i],y_cr[i],[7,7])
a.draw()
input()


