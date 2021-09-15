
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from pprint import pprint
import csv
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import numpy as np 
import matplotlib.collections as collections 

ts = TimeSeries(key='1NY7LKG2JYF48XIO', output_format='csv' )
aapl_csvreader, meta = ts.get_intraday_extended( 'PLTR', interval='1min', slice='year1month2')

with open('aapl.csv', 'w') as write_csvfile:
    writer = csv.writer(write_csvfile, dialect='excel')
    for row in aapl_csvreader:
        writer.writerow(row)
datar = pd.read_csv('aapl.csv')
print(datar)




count=0
supports= []
resistance= []
tsupports= 0
tresistance= 0

fig, ax = plt.subplots() 
ax.plot(datar['close'])
plt.gca().invert_xaxis()

balance=0
nshares=0
max=13690
max1=max+1
max2=max+2
highest=0
for x in range(max):
     polume = datar.iloc[max-x]
     time= datar.iloc[max-x]['time']
     volume= datar.iloc[max-x]['volume']
     price = datar.iloc[max-x]['close']
     open= datar.iloc[max-x]['open']
     high = datar.iloc[max-x]['high']
     low = datar.iloc[max-x]['low']
     popen = datar.iloc[max1-x]['open']
     mid = datar.iloc[max1-x]['close']
     end = datar.iloc[max2-x]['close']
     begc= ((price-mid)/60)*20+mid
     endc=((mid-end)/60)*40+end
     
     
     #print('time:'+ str(x))
     
    # if balance-1000>200:
        # break
     #elif 1000-balance>25 and balance>0:
        # break
     if balance>highest:
         highest=balance
     
     if x>0 and x<max:
         if x==1:
             balance=1000
             

         if mid<=endc and mid<begc:
             if mid in supports:
                 supports=[]
                 tsupports=mid
                 ax.plot((max1-x),mid, color='green', marker='o', markersize=5)
                 ax.plot((max1-x),begc, color='blue', marker='o', markersize=5)
                 ax.plot((max1-x),endc, color='purple', marker='o', markersize=5)
                 print("support is:")
                 print(mid)
                 #print(nshares)
                
             supports.append(mid)
             
         if mid>begc and mid>=endc:
             if mid in resistance and mid>tsupports:
                 resistance=[]
                 tresistance=mid
                 ax.plot((max1-x),mid, color='red', marker='o', markersize=5)
                 print("resistance is:")
                 print(mid)
                 #if balance==0:
                     #balance=nshares*price
                # print(endc)
                # print(mid)
                 #print(begc)
             resistance.append(mid)
         if x==max-1:
               print("close")
               print(polume)
               #print('')  
               balance=nshares*price
               #ax.plot((max-x),price, color='yellow', marker='o', markersize=5)
               
         elif  balance==0 :
             if price-tsupports>=.5:
               balance=nshares*price
               print("change1") 
               
               print('')
               #ax.plot((max-x),price, color='yellow', marker='o', markersize=5)
               
             elif price>=tresistance :
               print("change2") 
               
               print('')
               balance= nshares*price
               #ax.plot((max-x),price, color='yellow', marker='o', markersize=5)
         else:
             if price >=tsupports:
                 nshares=balance/price
                 balance=0
                 count+=1

              
            
             
         
     
         
        
         
         print('balance:'+ str(balance))
         
         print('')
    
     
 


print(tsupports)
print(tresistance)
print(balance)
print(highest)
print(count)
plt.show()


