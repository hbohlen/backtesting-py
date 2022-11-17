
# %%
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas_ta as ta
import pandas as pd
df = pd.read_csv("EURUSD_Candlestick_5_M_ASK_30.09.2019-30.09.2022.csv")
df.reset_index(inplace=True)
df.head()

# %%
df["Gmt time"] = df["Gmt time"].str.replace(".000", "")
df['Gmt time'] = pd.to_datetime(df['Gmt time'], format='%d.%m.%Y %H:%M:%S')
df.set_index("Gmt time", inplace=True)
df = df[df.High != df.Low]
len(df)

# %%
df["EMA200"] = ta.ema(df.Close, length=200)
df["EMA50"] = ta.ema(df.Close, length=50)
df["ATR"] = ta.atr(high=df.High, low=df.Low, close=df.Close, length=16)
df["RSI"] = ta.rsi(df.Close, length=16)
# help(ta.rsi)
df.tail()

# %%


def emasignal(df, backcandles):
    emasignal = [0]*len(df)

    for row in range(backcandles, len(df)):
        upt = 0
        dnt = 0

        for i in range(row - backcandles, row+1):
            if df.High[i] >= df.EMA200[i]:
                dnt = 0
            if df.Low[i] <= df.EMA200[i]:
                upt = 0
        if upt == 1 and dnt == 1:
            emasignal[row] = 3
        elif upt == 1:
            emasignal[row] = 2
        elif dnt == 1:
            emasignal[row] = 1

    df['EMASignal'] = emasignal


# %%
df.reset_index(drop=True, inplace=True)
emasignal(df, 6)


# %%
def totalsignal(df):
    ordersignal = [0]*len(df)

    for i in range(0, len(df)):
        if df.Close[i] >= df.EMA200[i]:
            ordersignal[i] = 1
    df['ordersignal'] = ordersignal


totalsignal(df)


# %%

def pointpos(x):
    if x['ordersignal'] == 2:
        return x['High']+2e-3

    elif x['ordersignal'] == 1:
        return x['Low']-2e-3

    else:
        return np.nan


df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)


# %%

dfpl = df[1000:3200]
dfpl.reset_index(drop=True, inplace=True)

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),
    go.Scatter(x=dfpl.index, y=dfpl.EMA200,
               line=dict(color='blue', width=1),
               name="EMA200")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=6, color="MediumPurple"),
                name="Signal")


# %%
