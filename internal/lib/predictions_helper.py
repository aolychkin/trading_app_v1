from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator


def condition(x):
  if 0.005 < x <= 1:
    return 2
  elif 0.002 <= x <= 0.005:
    return 1
  elif x < 0.002:
    return 0
  else:
    return -1


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
