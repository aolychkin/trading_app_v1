from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator


def condition(x):
  if 0.003 <= x:
    return 1  # 134419
  elif x < 0.003:
    return 0  # 311213

  # if 0.006 < x <= 1:
  #   return 3  # (0.005) 42236 -> 33078
  # elif 0.002 < x <= 0.006:
  #   return 2  # 92183 -> 101341
  # elif 0 < x < 0.002:
  #   return 1  # 187326
  # elif x <= 0:
  #   return 0  # 10953 + 112934 = 123887
  # else:
  #   return -2

  # 3    63686
  # 0    58655
  # 2    52540
  # 1    42855
  # 4    16739
  # -1   6304

  # if 0.006 <= x <= 1:
  #   return 4
  # elif 0.002 < x < 0.006:
  #   return 3
  # elif 0.001 <= x <= 0.002:
  #   return 2
  # elif 0 < x < 0.001:
  #   return 1
  # elif x == 0:
  #   return 0
  # elif x < 0:
  #   return -1
  # else:
  #   return -2


def w_max_10min():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df = pd.read_sql_query(
      "SELECT open, high, low, close, volume FROM candles", cnx)

  df["high_10min"] = df["high"].rolling(
      window=10, closed='right').max().shift(-10).fillna(0)
  df["pred_high"] = (df["high_10min"] / df["close"])-1
  df["pred_class"] = df["pred_high"].apply(condition)

  df.index += 1  # синхранизируем с id бд
  print(tabulate(df.loc[0:20], headers='keys', tablefmt='psql'))
  print(df["pred_class"].value_counts())

  return df

  # соединить с params потом, сделать dropna по rows
