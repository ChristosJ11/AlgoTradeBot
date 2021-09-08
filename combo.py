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
import csv
#datar = yf.download(tickers='PLTR', period='1d', interval='1m')
#--
ts = TimeSeries(key='1NY7LKG2JYF48XIO', output_format='csv' )
aapl_csvreader, meta = ts.get_intraday_extended( 'PLTR', interval='1min', slice='year1month1')

with open('aapl.csv', 'w') as write_csvfile:
    writer = csv.writer(write_csvfile, dialect='excel')
    for row in aapl_csvreader:
        writer.writerow(row)
datar = pd.read_csv('aapl.csv')

#--

def main(tick, balancey):
  length=len(datar.index)
  supports= []
  resistance= []
  fig, ax = plt.subplots() 
  ax.plot(datar['close'])
  
  highest=0
  nshares=0
  prices=[]
  balance=0
  count=0
  uptrend= True
  for x in range(length):
        polume = datar.iloc[x]
        
        nround=round(nshares)
        #print(datar.iloc[80-x]['close'])
        #if balance-100>200:
        #break
        #elif 1000-balance>25 and balance>0:
        # break
        if balance>highest:
         highest=balance
      
        if x>4 and x<length:
                price = datar.iloc[length-x]['close']
                mid = datar.iloc[length-x+1]['close']
                end = datar.iloc[length-x+2]['close']
                begc= ((price-mid)/60)*30+mid
                endc=((mid-end)/60)*30+end
                if mid<=endc and mid<begc:
                    supports.append(mid)
                    print("bru")
                    if supports[len(supports)-1]<=mid and supports[len(supports)-2]<=mid:
                        uptrend=True
                        print("support is:")
                        print(price)
                    else:
                        uptrend=False
                        
                        
                    
                if x==5:
                    prices.append(price)
                    sma=sum(prices)/1
                    balance=1000
                    pema=sma
                elif x>6:
                    ema=price*(2/(1+x+6))+(pema*(1-(2/(1+x+6))))
                    print("THIS IS EMA:"+ str(ema))
                    datar.loc[datar.index[length-x], 'ema'] = str(ema)
                    pema=ema
                    print(str(price)+"vs"+str(ema))
                    #ax.plot((80-x),ema, color='blue', marker='o', markersize=1)

                if x==length-1 and balance==0:
                        print(" this is close")
                        print(polume)
                        print('')  
                        print(nshares)
                        
                        balance=nshares*price
                elif uptrend==False and price>ema and balance==0:
                        
                        balance=nshares*price
                elif x>7:
                  if uptrend==True and balance!=0 and price<ema:
                       nshares=balance/price
                       balance=0
                       ax.plot((length-x),mid, color='red', marker='o', markersize=5)
                       print("buy plz")
                print(balance)     
                      
                    
                                          
  print("balance is:"+ str(balance))
  #ax.plot(datar["sell"])
  ax.plot(datar["ema"])
  plt.gca().invert_xaxis()
  plt.show()


main(0, 10)
'''                   
                if uptrend==True or x==length-1:
                    if x==length-1 and balance==0:
                        print(" this is close")
                        print(polume)
                        print('')  
                        print(nshares)
                        balance=nshares*price
                    if  balance==0 and x!=1 and nshares!=0:
                        if price>=ema or x==length-5:
                            print(nround)
                            balance=nshares*price
                            print("change2") 
                            print(polume)
                            print(str(price)+"vs"+str(ema))
                            print('balance is:'+ str(balance))
                            print('')
                            datar.loc[datar.index[x], 'sell'] = str(price)  

                    if balance != 0 and x!=1 and x!=length-1:
                        if price<=ema:
                            nshares=balance/price
                            balance=0
                            print(polume)
                            print('nshare:'+str(nshares))
                            print(str(price)+"vs"+str(ema))
                            print('balance is:'+ str(balance))
                            print('')
                            count+=1
'''  