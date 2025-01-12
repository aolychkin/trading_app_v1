from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm

import sqlite3
import pandas as pd
import numpy as np


def cross(s_MACD, f_MACD, s_signal, f_signal):
  y1 = 1
  y2 = 2
  y3 = 1
  y4 = 2
  n = 0
  down_up = -1
  if (y2 - y1 != 0):
    q = (f_MACD - s_MACD) / (y1 - y2)
    sn = (s_signal - f_signal) + (y3 - y4) * q
    if (not sn):
      return 0
    fn = (s_signal - s_MACD) + (y3 - y1) * q
    n = fn / sn
  else:
    n = (y3 - y1) / (y3 - y4)

  dot2 = y3 + (y4 - y3) * n
  if (1 <= dot2 <= 2):
    if (dot2 == 2):
      down_up = 1 if (s_MACD/s_signal-1 < 0) else 0
    elif (dot2 == 1):
      down_up = 1 if (f_MACD/f_signal-1 > 0) else 0
    else:
      down_up = 1 if (s_MACD/s_signal-1 < 0) else 0
  else:
    down_up = -1

  if down_up == 1:
    return 1  # покупать
  elif down_up == 0:
    return -1  # продавать
  else:
    return 0


def macd():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')
  df = pd.read_sql_query(
      "SELECT MACD10_signal, MACD12_24 FROM indicators", cnx)

  df.insert(loc=0, column='MACD10_pred', value=df["MACD10_signal"].shift(1))
  df.insert(loc=2, column='MACD12_24_pred', value=df["MACD12_24"].shift(1))
  df.drop(0, inplace=True)
  df["cross_type"] = df.apply(lambda row: cross(row["MACD12_24_pred"], row["MACD12_24"], row["MACD10_pred"], row["MACD10_signal"]), axis=1)
  df["counter"] = 0
  for i in tqdm(range(1, len(df))):
    power = np.abs(np.mean([df.loc[i, "MACD12_24_pred"], df.loc[i, "MACD12_24"]]) / np.mean([df.loc[i, "MACD10_pred"], df.loc[i, "MACD10_signal"]]) - 1)
    if df.loc[i, 'cross_type'] == 0:
      counter = df.loc[i-1, 'counter'] + 1
      tmp_pred_power = df.loc[i-1, 'tmp_power']
      df.loc[i, 'counter'] = counter
      df.loc[i, 'tmp_power'] = tmp_pred_power
      if (df.loc[i, 'tmp_power'] > 0):
        df.loc[i, 'power'] = tmp_pred_power - df.loc[i-counter, "cross_type"] * np.sqrt(np.abs(np.sqrt(counter) * tmp_pred_power * np.sqrt(power)))
        # df.loc[i, 'power'] = power
      elif (df.loc[i, 'tmp_power'] < 0):
        df.loc[i, 'power'] = tmp_pred_power - df.loc[i-counter, "cross_type"] * np.sqrt(np.abs(np.sqrt(counter) * tmp_pred_power * np.sqrt(power)))
        # df.loc[i, 'power'] = power
    else:
      df.loc[i, 'counter'] = 0
      df.loc[i, 'tmp_power'] = df.loc[i, "cross_type"] * power
      df.loc[i, 'power'] = df.loc[i, "cross_type"] * power

  df.index += 1  # синхранизируем с id бд
  # print(df["power"].head())
  # print(tabulate(df.loc[220:270], headers='keys', tablefmt='psql'))
  # print(df["cross_type"].value_counts())
  print("MACD:", df["power"].min(), df["power"].max())
  return (df["power"])


def rsi():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')
  df = pd.read_sql_query(
      "SELECT id, RSI9 FROM indicators", cnx)

  df.insert(loc=0, column='RSI9_pred', value=df["RSI9"].shift(1))
  df["cross_type"] = df.apply(lambda row: cross(row["RSI9_pred"], row["RSI9"], 70, 70), axis=1)
  df["counter"] = 0

  for i in tqdm(range(1, len(df))):
    power = np.abs(np.mean([df.loc[i, "RSI9_pred"], df.loc[i, "RSI9"]]) / 70 - 1)
    counter = df.loc[i, 'cross_type']
    if df.loc[i, 'cross_type'] == 0:
      counter = df.loc[i-1, 'counter']
      df.loc[i, 'counter'] = counter
      df.loc[i, 'power'] = counter * power
      if counter == 0:
        df.loc[i, 'power'] = -power
    elif df.loc[i, 'cross_type'] == 1:
      df.loc[i, 'counter'] = counter
      df.loc[i, 'power'] = 1 - power
    else:
      df.loc[i, 'counter'] = counter
      df.loc[i, 'power'] = -1 + power

  df.drop(0, inplace=True)
  df.index += 1  # синхранизируем с id бд
  # print(tabulate(df.loc[421910:421930], headers='keys', tablefmt='psql'))
  # print(tabulate(df.loc[df[df["RSI9"] >= 70].iloc[0]["id"]-2:320], headers='keys', tablefmt='psql'))
  # print(tabulate(df.head(), headers='keys', tablefmt='psql'))
  # print(df["cross_type"].value_counts())
  print("RSI:", df["power"].min(), df["power"].max())
  return (df["power"])


def adx():  # Растущий и высокий тренд (больше 25 и чем больше - тем лучше) = подтверждение продажи и покупки. "Для ADX все что не рост - все слабость тренда"
  cnx = sqlite3.connect('./storage/sqlite/shares.db')
  df = pd.read_sql_query(
      "SELECT ADX9 FROM indicators", cnx)

  df.insert(loc=0, column='ADX9_pred', value=df["ADX9"].shift(1))

  for i in tqdm(range(1, len(df))):
    if df.loc[i, 'ADX9'] >= 25:
      df.loc[i, 'power'] = df.loc[i, 'ADX9'] / df.loc[i, 'ADX9_pred'] - 1
    else:
      df.loc[i, 'power'] = -1 + np.abs(df.loc[i, 'ADX9'] / df.loc[i, 'ADX9_pred'] - 1)

  df.drop(0, inplace=True)
  df.index += 1  # синхранизируем с id бд
  # print(tabulate(df.loc[220:270], headers='keys', tablefmt='psql'))
  print("ADX:", df["power"].min(), df["power"].max())

  return (df["power"])
