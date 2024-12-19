import json
from datetime import datetime, timedelta
import akshare as ak

import numpy as np
import yfinance as yf
import pandas as pd
from prettytable import PrettyTable

tickers = [
    {'ticker': '510050.SS', 'name': '上证50'},    #0.2~0.3
    {'ticker': '159601.SZ', 'name': 'A50'},    #0.2~0.3
#    {'ticker': '510300.SS', 'name': '沪深300'},
#    {'ticker': '159628.SZ', 'name': '国证2000'},
    {'ticker': '159948.SZ', 'name': '创业板'},   #0.3

    {'ticker': '512660.SS', 'name': '中证军工'},  #0.4~0.5
    {'ticker': '512710.SS', 'name': '军工龙头'},  #0.4

    {'ticker': '159851.SZ', 'name': '金融科技'},  #0.6
    {'ticker': '159899.SZ', 'name': '软件指数'},  #0.4~0.5
    {'ticker': '515880.SS', 'name': '通信设备'},  #0.4
    {'ticker': '516510.SS', 'name': '云计算'},    #0.5
    {'ticker': '159813.SZ', 'name': '国证芯片'},

    {'ticker': '515700.SS', 'name': '新能车'},    #0.4
    {'ticker': '159857.SZ', 'name': '光伏产业'}, #0.4~0.5

    {'ticker': '588210.SS', 'name': '科创100'},  #0.5
    {'ticker': '588290.SS', 'name': '科创芯片'}, #0.6
    {'ticker': '588830.SS', 'name': '科创新能源'}, #0.5~0.6
    {'ticker': '588680.SS', 'name': '科创医药'},  #0.5
    {'ticker': '588010.SS', 'name': '科创材料'}, #0.5

    {'ticker': '513280.SS', 'name': '港股医药'},  #0.3
    {'ticker': '159699.SZ', 'name': '港股消费'},
    {'ticker': '513130.SS', 'name': '恒生科技'},  #0.3

    {'ticker': '159847.SZ', 'name': '中证医疗'},  #0.3
    {'ticker': '159837.SZ', 'name': '生物科技'},
    {'ticker': '512010.SS', 'name': '300医药'},
    {'ticker': '159928.SZ', 'name': '中证消费'},  #0.3

    {'ticker': '512880.SS', 'name': '全指证券'},
#    {'ticker': '512400.SS', 'name': '有色金属'},  #0.3
#    {'ticker': '515220.SS', 'name': '中证煤炭'},
#    {'ticker': '159667.SZ', 'name': '中证机床'},  #0.3~0.4

#    {'ticker': '513360.SS', 'name': '中国教育'},
    {'ticker': '516770.SS', 'name': '动漫游戏'}, #0.5
    {'ticker': '159855.SZ', 'name': '中证影视'},  #0.4
    {'ticker': '159805.SZ', 'name': '中证传媒'},   #0.4~0.5

    {'ticker': '163406.SZ', 'name': '兴全合润'},

    {'ticker': '300274.SZ', 'name': '阳光电源'},
    {'ticker': '600438.SS', 'name': '通威股份'},
]

#5分钟数据，最近3个交易日汇总, 150个点
def getData2(t):
    if (t.find('SZ') != -1):
        t = 'sz' + t
    else:
        t = 'sh' + t
    t = t.replace('.SZ', '')
    t = t.replace('.SS', '')

    stock_zh_a_spot_df = ak.stock_zh_a_minute(symbol=t, period='5', adjust='qfq')
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    print(stock_zh_a_spot_df.head(5))
    print(stock_zh_a_spot_df.tail(5))
    stock_zh_a_spot_df['Return'] = stock_zh_a_spot_df['close'].astype(float).pct_change()
    volatility = np.std(stock_zh_a_spot_df['Return'].dropna())
    annual_volatility = volatility * np.sqrt(252 * 4.5 * 4 * 3)
    print(annual_volatility)
    return annual_volatility

def getData(t):
    current = datetime.now() + timedelta(days=1)
    last_30_day = current - timedelta(days=7)

    data = yf.download(t, start=last_30_day.strftime('%Y-%m-%d'), end=current.strftime('%Y-%m-%d'), interval='15m')
    #print(data.tail(5))
    print(data['Adj Close'])

    data['Return'] = data['Adj Close'].pct_change()
    volatility = np.std(data['Return'].dropna())
    annual_volatility = volatility * np.sqrt(252 * 4.5 * 4)
#    print(f" volatility: {annual_volatility}")
    return annual_volatility


for tt in tickers:
#    tt['volatility'] = getData(tt.get('ticker'))
    tt['volatility'] = getData2(tt.get('ticker')) * 20000

sorted_dict = sorted(tickers, key=lambda x : x['volatility'])

table = PrettyTable()
table.field_names = ["Code", "Name", "5", "10", "20"]

# 输出排序后的字典
for tt in sorted_dict:
    table.add_row([tt['ticker'], tt['name'], tt['volatility'] / 2, tt['volatility'], tt['volatility'] * 2])

print(table)