
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
POSITIONS_URL="{}/v2/positions".format(BASE_URL)
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
def get_position(symbol):
    data={
        "symbol":symbol
    }
    r=requests.get(POSITIONS_URL,json=data, headers=HEADERS)
    return json.loads(r.content)
#end of creds------------------------------------------------



count=0
#drow= datar.head()
#dlist= drow.index.values.tolist()
tick="PLTR"
print(get_account())

nshares=0
while True:
    sleep(60)
    datar = yf.download(tickers=tick, period='7d', interval='1m')
    length=len(datar.index)
    
    supports= []
    resistance= []
    tsupports= 0
    tresistance= 0
    account=get_account()
    positiony=get_position(tick)
    balance=int(float(account['cash']))
    
 
    for x in range(length):
     polume = datar.iloc[x]
     price = datar.iloc[x]['Close']
     mid = datar.iloc[x-1]['Close']
     end = datar.iloc[x-2]['Close']
     begc= ((price-mid)/60)*20+mid
     endc=((mid-end)/60)*40+end
     
     
     
    
     
     if x>0 and x<length:
       
         if mid<=endc and mid<begc:
             if mid in supports:
                 supports=[]
                 tsupports=mid
                 print("support is:")
                 print(mid)
                 #print(nshares)
                
             supports.append(mid)
             
         if mid>begc and mid>=endc:
             if mid in resistance and mid>tsupports:
                 resistance=[]
                 tresistance=mid
                 print("resistance is:")
                 print(mid)
             resistance.append(mid)

    nprice= datar.iloc[length-1]['Close']                  
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    
    if current_time=="14:58:00" :
        quantity=int(float(positiony[0]["qty"]))
        print(quantity)
        print("close")
        nround=round(nshares)
        create_order(tick,quantity, "sell", "market", "gtc")
        print('')  
        
        

    elif  balance<price :
             quantity=int(float(positiony[0]["qty"]))
             print(quantity)
             if price-tsupports>=.5:
               create_order(tick,quantity, "sell", "market", "gtc") 
               print("change1") 
               print('')
            
             elif price>=tresistance :
               print("change2") 
               create_order(tick,quantity, "sell", "market", "day")
               print('')
               
               
    else:
             if price >=tsupports and balance!=0:
                 nshares=balance/price
                 nround=round(nshares)
                 create_order(tick,nround, "buy", "market", "gtc")
                 print("I'm buying")
                 count+=1

                           
    

#ends  here ----
 
 




