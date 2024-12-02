import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from arch import arch_model

#ticker = '516080.SS'
tickers = [
#    {'ticker': '159851.SZ', 'name': '金融科技'},
#    {'ticker': '588290.SS', 'name': '科创芯片'},
    {'ticker': '516770.SS', 'name': '动漫游戏'},
#    {'ticker': '159899.SZ', 'name': '软件指数'},
#    {'ticker': '588680.SS', 'name': '科创100'},
#    {'ticker': '515880.SS', 'name': '通信设备'},
#    {'ticker': '161628.SZ', 'name': '云计算'},
#    {'ticker': '159755.SZ', 'name': 'CS电池'},
    {'ticker': '159847.SZ', 'name': '中证医疗'},
    {'ticker': '510300.SS', 'name': '沪深300'},
#    {'ticker': '510050.SS', 'name': '上证50'},
#    {'ticker': '513010.SS', 'name': '恒生科技'},
    {'ticker': '512660.SS', 'name': '中证军工'},
#    {'ticker': '159805.SZ', 'name': '中证传媒'},
#    {'ticker': '159628.SZ', 'name': '国证2000'},
#    {'ticker': '159928.SZ', 'name': '中证消费'},
#    {'ticker': '159857.SZ', 'name': '光伏产业'},
    {'ticker': '159915.SZ', 'name': '创业板'},
]


def getData(t):
    data = yf.download(t, start='2018-12-01', end='2024-12-28', interval='1d')
    print(data.head())

    data['Return'] = data['Adj Close'].pct_change()
    daily_volatility = np.std(data['Return'].dropna())
    annual_volatility = daily_volatility * np.sqrt(252)
    print(f"Annual Volatility: {annual_volatility}")

    window_size = 30  # 30天滚动窗口
    return data['Return'].rolling(window=window_size).std() * np.sqrt(252)

plt.rcParams['font.family'] = 'Heiti TC'
plt.figure(figsize=(10, 6))
for tt in tickers:
    plt.plot(getData(tt.get('ticker')), label=tt.get('name'))
plt.title('Rolling Volatility Over Time')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()





#model = arch_model(data['Return'].dropna(), vol='Garch', p=1, q=1)
#model_fit = model.fit(disp='off')
#print(model_fit.summary())

