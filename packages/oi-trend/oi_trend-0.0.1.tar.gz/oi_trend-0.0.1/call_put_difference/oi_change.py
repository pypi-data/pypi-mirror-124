import yfinance as yf 
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import math
import matplotlib.pyplot as plt
from datetime import datetime
import nsepython as np_nse
import time

from matplotlib.animation import FuncAnimation
#index = 'BANKNIFTY'

s_PE_list = []
s_CE_list = []
s_dif_list = []
current_time_list = []
s_IV_PE_list = []
s_IV_CE_list = []
pcr_list = []

def nse_option_chain_data(index):
    #print(np_nse.nse_optionchain_scrapper(index))
    data = np_nse.nse_optionchain_scrapper(index)
    return data['records']['data']

def current_time_list_func():
# datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M:%S")
    print("current_time =", dt_string)
    current_time_list.append(dt_string)
    return current_time_list

def latest_expiry_date(index):
    data = np_nse.nse_optionchain_scrapper(index)
    return data['records']['expiryDates'][0]

latest_expiry_date = latest_expiry_date("BANKNIFTY")

def rounded_price(index):
    
    s=math.ceil(np_nse.nse_quote_ltp(index))
    #print(s)

    check = s%100

    if check<=50:
        ans= s%100
        s =s -ans
    else: 
        ans= 100-s%100
        s =s +ans

    #print(s)
    return s

def PE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date):
    s_PE=0
    s_IV_PE =0
    
    for i in records_data:
        try:
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price-100) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price-200) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price-300) :
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price-400) :
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price-500) :
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price) :
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price+100) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price+200) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price+300) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price+400) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )
            if(i['PE']['expiryDate']==latest_expiry_date and i['PE']['strikePrice']==live_bnf_price+500) :
                s_PE=s_PE+i['PE']['changeinOpenInterest']
                s_IV_PE = s_IV_PE+ i['PE']['impliedVolatility']
                #print(str(i['PE']['expiryDate'])+' '+str(i['PE']['strikePrice']) + ' ' +str(i['PE']['changeinOpenInterest']) + ' '+ str(i['PE']['openInterest']) )



        except:
            print('data not found')
    #print(s_PE)
    s_PE_list.append(s_PE)
    #print(s_IV_PE)
    s_IV_PE_list.append(s_IV_PE)
    
    d = dict(); 
    d['s_PE'] = s_PE
    d['s_PE_list'] = s_PE_list
    d['s_IV_PE_list']   = s_IV_PE_list
    return d


def CE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date):
    s_CE=0
    s_IV_CE =0
    for i in records_data:
        try:
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price-100):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price-200):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price-300):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price-400):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price-500):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price+100):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price+200):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price+300):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price+400):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )
            if(i['CE']['expiryDate']==latest_expiry_date and i['CE']['strikePrice']==live_bnf_price+500):
                s_CE=s_CE+i['CE']['changeinOpenInterest']
                s_IV_CE = s_IV_CE+ i['CE']['impliedVolatility']
                #print(str(i['CE']['expiryDate'])+' '+str(i['CE']['strikePrice']) + ' ' +str(i['CE']['changeinOpenInterest']) + ' '+ str(i['CE']['openInterest']) )    

        except:
            print('data not found')
    #print(s_CE)
    s_CE_list.append(s_CE)
    #print(s_IV_CE)
    s_IV_CE_list.append(s_IV_CE)
    
    d = dict(); 
    d['s_CE'] = s_CE
    d['s_CE_list'] = s_CE_list
    d['s_IV_CE_list']   = s_IV_CE_list
    return d





def diagram_s_dif_list(current_time_list,s_dif_list):
    x = current_time_list
    y = s_dif_list
    print("x"  + str(x))
    print("y"  + str(y))

    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(10)
    plt.plot(x, y)
    plt.xlabel("Time")  # add X-axis label
    plt.ylabel("Difference between put and call")  # add Y-axis label
    plt.title("Banknifty")  # add title
    plt.show()



def imp(index):
    #latest_expiry_date=latest_expiry_date(index)
    records_data = nse_option_chain_data(index)
    live_bnf_price=rounded_price('BANKNIFTY')
    y = CE_chnageinOi_IV(records_data)
    x = PE_chnageinOi_IV(records_data)
    s_dif_list.append(x['s_PE']-y['s_CE'])
    current_time_list=current_time_list_func()
    payload=np_nse.nse_optionchain_scrapper(index)
    #print(np_nse.pcr(payload,0))

    pcr_list.append(np_nse.pcr(payload,0))
    
    
    diagram_s_dif_list(current_time_list,s_dif_list)
    
  
# while(True):
    
#     imp('BANKNIFTY')
#     time.sleep(240)

def animate(i,index):
    if index == "BANKNIFTY":
        print(index)
        records_data = nse_option_chain_data('BANKNIFTY')
        live_bnf_price=rounded_price('BANKNIFTY')
        
        #print(records_data)
        y1 = CE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date)
        x1 = PE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date)
        print(live_bnf_price)

        s_dif_list.append(x1['s_PE']-y1['s_CE'])
        current_time_list=current_time_list_func()


        x = current_time_list
        y = s_dif_list
        # print("x"  + str(x))
        # print("y"  + str(y))

        # f = plt.figure()
        # f.set_figwidth(20)
        # f.set_figheight(10)
        # plt.plot(x, y)
        # plt.xlabel("Time")  # add X-axis label
        # plt.ylabel("Difference between put and call")  # add Y-axis label
        # plt.title("Banknifty")  # add title
        # plt.show()

        
        
        plt.cla()
        
        plt.plot(x,y)

        plt.xlabel("Time")  # add X-axis label
        plt.ylabel("Difference between put and call")  # add Y-axis label
        plt.title("Banknifty")  # add title



    if index == "NIFTY":
        records_data = nse_option_chain_data('NIFTY')
        live_bnf_price=rounded_price('NIFTY')
        
        y1 = CE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date)
        x1 = PE_chnageinOi_IV(records_data,live_bnf_price,latest_expiry_date)

        s_dif_list.append(x1['s_PE']-y1['s_CE'])
        current_time_list=current_time_list_func()


        x = current_time_list
        y = s_dif_list
        # print("x"  + str(x))
        # print("y"  + str(y))

        # f = plt.figure()
        # f.set_figwidth(20)
        # f.set_figheight(10)
        # plt.plot(x, y)
        # plt.xlabel("Time")  # add X-axis label
        # plt.ylabel("Difference between put and call")  # add Y-axis label
        # plt.title("Banknifty")  # add title
        # plt.show()

        
        
        plt.cla()
        
        plt.plot(x,y)

        plt.xlabel("Time")  # add X-axis label
        plt.ylabel("Difference between put and call")  # add Y-axis label
        plt.title("Nifty")  # add title

def trend(index):
    ani = FuncAnimation(plt.gcf(),animate,interval = 240000,fargs=(index,))
    plt.show()

    