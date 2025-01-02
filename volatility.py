from datetime import datetime, timedelta

import akshare as ak
import numpy as np
import pandas as pd
import yfinance as yf
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from prettytable import PrettyTable

tickers = [
    {'ticker': '510050.SS', 'name': '上证50'},
    {'ticker': '159595.SZ', 'name': 'A50'},
    {'ticker': '163406.SZ', 'name': '兴全合润'},
#    {'ticker': '510300.SS', 'name': '沪深300'},
    {'ticker': '563300.SS', 'name': '中证2000'},
    {'ticker': '159915.SZ', 'name': '创业板'},

    {'ticker': '512170.SS', 'name': '中证医疗'},
    {'ticker': '159837.SZ', 'name': '生物科技'},
    {'ticker': '512010.SS', 'name': '300医药'},
    {'ticker': '159928.SZ', 'name': '中证消费'},

    {'ticker': '512880.SS', 'name': '全指证券'},

    {'ticker': '159892.SZ', 'name': '港股医药'},
    {'ticker': '159699.SZ', 'name': '港股消费'},
    {'ticker': '513130.SS', 'name': '恒生科技'},

    {'ticker': '512660.SS', 'name': '中证军工'},
    {'ticker': '512710.SS', 'name': '军工龙头'},

    {'ticker': '515700.SS', 'name': '新能车'},
    {'ticker': '515790.SS', 'name': '光伏产业'},

    {'ticker': '159851.SZ', 'name': '金融科技'},
    {'ticker': '515230.SS', 'name': '软件指数'},
    {'ticker': '159732.SZ', 'name': '消费电子'},
    {'ticker': '515880.SS', 'name': '通信设备'},
    {'ticker': '516510.SS', 'name': '云计算'},
    {'ticker': '159995.SZ', 'name': '国证芯片'},

    {'ticker': '588200.SS', 'name': '科创芯片'},
    {'ticker': '588830.SS', 'name': '科创新能源'},
    {'ticker': '588860.SS', 'name': '科创医药'},
    {'ticker': '588010.SS', 'name': '科创材料'},
    {'ticker': '588100.SS', 'name': '科创信息技术'},
    {'ticker': '588030.SS', 'name': '科创100'},

#    {'ticker': '512400.SS', 'name': '有色金属'},
#    {'ticker': '515220.SS', 'name': '中证煤炭'},
#    {'ticker': '159667.SZ', 'name': '中证机床'},

#    {'ticker': '513360.SS', 'name': '中国教育'},
    {'ticker': '159869.SZ', 'name': '动漫游戏'},
    {'ticker': '159855.SZ', 'name': '中证影视'},
    {'ticker': '512980.SS', 'name': '中证传媒'},

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
    tt['volatility'] = int(getData2(tt.get('ticker')) * 20000)

#sorted_dict = sorted(tickers, key=lambda x : x['volatility'])
sorted_dict = tickers

table = PrettyTable()
table.field_names = ["Code", "Name", "5", "10", "20"]

# 输出排序后的字典
for tt in sorted_dict:
    table.add_row([tt['ticker'], tt['name'], tt['volatility'] / 2, tt['volatility'], tt['volatility'] * 2])

# 将PrettyTable转换成字符串
table_str = str(table)

# 设置图片大小，需要足够大以容纳文本
image_width = 500
image_height = 1000

# 创建一个新的白色图片
image = Image.new('RGB', (image_width, image_height), color='white')
font = ImageFont.truetype('STHeiti Light.ttc', 18)
draw = ImageDraw.Draw(image)

y = 5
for line in table_str.splitlines():
    draw.text((5, y), line, font=font, fill=(0, 0, 0))
    y += 20  # 15是行高，根据字体大小调整

# 保存图片
image.save('table.png')

print(table)
