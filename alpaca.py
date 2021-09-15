
from time import time, sleep
import plotly.graph_objs as go
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from pprint import pprint
import json
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import numpy as np 
import matplotlib.collections as collections 
import requests
from sample_config import *
from datetime import datetime

ts = TimeSeries(key='1NY7LKG2JYF48XIO', output_format='pandas' )
app = TechIndicators(key='1NY7LKG2JYF48XIO',output_format='pandas')

#-----------------------------------------------------------
BASE_URL='https://paper-api.alpaca.markets'
ACCOUNT_URL="{}/v2/account".format(BASE_URL)
ORDERS_URL="{}/v2/orders".format(BASE_URL)
HEADERS={'APCA-API-KEY-ID':API_KEY,'APCA-API-SECRET-KEY':SECRET_KEY}
def get_account():
    r= requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data={
        "symbol": symbol,
        "qty":qty,
        "side":side,
        "type":type,
        "time_in_force": time_in_force,

    }
    r=requests.post(ORDERS_URL,json=data ,headers=HEADERS)
    return json.loads(r.content)


#end of creds------------------------------------------------


count=0
supports= []
resistance= []
tsupports= 0
tresistance= 0
fig, ax = plt.subplots() 
#ax.plot(datar['Close'])
nshares=0
prices=[]
highest=0
#drow= datar.head()
#dlist= drow.index.values.tolist()
tick="PLTR"
balance=600
while True:
    sleep(60)
    datar = yf.download(tickers=tick, period='50d', interval='15m')
    length=len(datar.index)
    print(length)
    for x in range(length):
            polume = datar.iloc[x]
            price = datar.iloc[x]['Close']
            mid = datar.iloc[x]['Close']
            end = datar.iloc[x]['Close']
            begc= ((price-mid)/60)*30+mid
            endc=((mid-end)/60)*30+end
            
            
            
        
            if x>0 and x<length:
                    
                    #ax.plot((80-x),sma, color='purple', marker='o', markersize=1)
                    if x==1:
                        sma=sum(prices)/x
                        pema=sma
                    else:
                        ema=price*(2/(1+x))+(pema*(1-(2/(1+x))))
                        #print("THIS IS EMA:"+ str(ema))
                        datar.loc[datar.index[x], 'ema'] = str(ema)
                        pema=ema
                        #print(str(price)+"vs"+str(ema))
                        #ax.plot((80-x),ema, color='blue', marker='o', markersize=1)

    nprice= datar.iloc[length-1]['Close']                  
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    print("THIS IS EMA:"+ str(ema))
    print(nprice)
    if current_time=="16:00:00" and nshares!=0:
        print("close")
        nround=round(nshares)
        create_order(tick,nround, "sell", "market", "gtc")
        print('')  
        balance=nshares*price
        #ax.plot((80-x),price, color='yellow', marker='o', markersize=3)

    if balance != 0 :
        if nprice<=ema:
            nshares=balance/nprice
            nround=round(nshares)
            create_order(tick,nround, "buy", "market", "gtc")
            balance=0
            print("I'm buying")
            print('nshare:'+str(nshares))
            print(str(nprice)+"vs"+str(ema))
            print('balance is:'+ str(balance))
            print('')
            count+=1
        
    if  balance==0 and nshares!=0:
        if nprice>=ema or current_time=="16:00:00":
            nround=round(nshares)
            create_order(tick,nround, "sell", "market", "gtc")
            balance=nshares*nprice
            print("change2") 
            print("im selling ")
            print(str(nprice)+"vs"+str(ema))
            print('balance is:'+ str(balance))
            print('')
                                #ax.plot((x),price, color='yellow', marker='o', markersize=3)
                #print(balance)
                #print(polume)


#ends  here ----
'''  
     if x>0 and x<80:
         if x==1:
             balance=100
             

         if mid<=endc and mid<begc:
             if mid in supports:
                 supports=[]
                 tsupports=mid
                 ax.axhline(mid, color="green")
                 print("support is:")
                 print(nshares)
                 print(iprice)
                 if balance != 0:
                     nshares=balance/price
                     iprice=price
                     balance=0
             supports.append(mid)
             
         if mid>begc and mid>=endc:
             if mid in resistance:
                 resistance=[]
                 tresistance=mid
                 ax.axhline(mid, color="red")
                 print("resistance is:")
                 print(price)
                 print(endc)
                 print(mid)
                 print(begc)
             resistance.append(mid)
         if balance==0:
             if x==79:
               balance=nshares*price
             elif price>tresistance and price<mid:
               balance= nshares*price
             elif price<tresistance:
               balance=nshares*price

         
     
      
     #print(polume)
    
'''     
 



print(balance)
#ax.plot(datar["ema"])
#plt.show()


#we can use th volume function to see when resistance occurs
#I can also store the value where resistance occurs last for the future
#volume=datar['2021-02-16 '+str(dog)+':'+str(c)+':00 ']['5. volume']
