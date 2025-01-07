from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from ta.trend import ADXIndicator

from domain import models

# Утренняя торговая сессия: 04:00 – 7:00 utc.
s_morning = datetime(2024, 12, 2, 4, 00).strftime("%H:%M")
f_morning = datetime(2024, 12, 2, 7, 00).strftime("%H:%M")

# Основная торговая сессия: 7:00 – 16:00 utc.
s_main = datetime(2024, 12, 2, 7, 00).strftime("%H:%M")
f_main = datetime(2024, 12, 2, 16, 00).strftime("%H:%M")

# Дополнительная торговая сессия: 16:00 – 20:50 utc.
s_evening = datetime(2024, 12, 2, 16, 00).strftime("%H:%M")
f_evening = datetime(2024, 12, 2, 20, 50).strftime("%H:%M")


def w_session(candle_time):
  # В какую торговую сессию торгуется свеча (what)
  if (s_morning < candle_time <= f_morning):
    return 0
  elif (s_main < candle_time <= f_main):
    return 1
  elif (s_evening < candle_time <= f_evening):
    return 2
  else:
    return -1


def w_s_min(candle_time):
  # Сколько времени прошло от начала текущей торговой сессии (what)
  if (s_morning <= candle_time <= f_morning):
    return int((datetime.strptime(candle_time, "%H:%M") -
                datetime.strptime(s_morning, "%H:%M")).seconds/60)
  elif (s_main < candle_time < f_main):
    return int((datetime.strptime(candle_time, "%H:%M") -
                datetime.strptime(s_main, "%H:%M")).seconds/60)
  elif (s_evening <= candle_time <= f_evening):
    return int((datetime.strptime(candle_time, "%H:%M") -
                datetime.strptime(s_evening, "%H:%M")).seconds/60)
  else:
    return -1


# def w_dm(candle_c: models.Candles, candle_p: models.Candles):
#   # расчет +-M
#   p_m = candle_c.high - candle_p.high
#   m_m = candle_p.low - candle_c.low

#   # расчет +-DM
#   p_dm = p_m if (p_m > m_m and p_m > 0) else 0
#   m_dm = m_m if (m_m > p_m and m_m > 0) else 0

#   tr = max(candle_c.high, candle_p.close) - min(candle_c.low, candle_p.close)

#   return tr, p_dm, m_dm


def w_all_ema():  # расчет EMA. Нужно будет в этой оболочке и вести запись в родительском файле
  cnx = sqlite3.connect('./storage/sqlite/shares.db')
  df = pd.read_sql_query("SELECT volume, high, low, close FROM candles", cnx)
  # TODO: close context

  # простой расчет volume
  df["volume-1"] = df["volume"].shift(periods=1)
  df["md_volume"] = df["volume"].diff(periods=1).fillna(0)/df["volume-1"]

  # смещение close на 1 назад, чтобы использовать для расчета прошлых свечей
  df["close-1"] = df["close"].shift(periods=1)
  # расчет +-M
  df["p_M"] = df['high'].diff().fillna(0)
  df["m_M"] = df['low'].diff(
      periods=1).apply(lambda x: x if x == 0 else x*-1).fillna(0)

  # расчет TR
  df["TR"] = np.max(
      df[["high", "close-1"]].values, axis=1) - np.min(df[["low", "close-1"]].values, axis=1)

  # расчет +-DM
  df["p_DM"] = np.where(
      (df['p_M'] > df['m_M']) & (df['p_M'] > 0), df['p_M'], 0)
  df["m_DM"] = np.where(
      (df['m_M'] > df['p_M']) & (df['m_M'] > 0), df['m_M'], 0)

  # расчет +-DI
  df["p_DI9"] = (df['p_DM']/df['TR']).ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)
  df["m_DI9"] = (df['m_DM']/df['TR']).ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)

  # расчет всяких EMA
  df["EMA9"] = df['close'].ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)
  df["EMA9_GAIN"] = df['close'].diff().clip(lower=0).ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)
  df["EMA9_LOSS"] = df['close'].diff().clip(
      upper=0).apply(lambda x: x if x == 0 else x*-1).ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)

  df["EMA9_ABS_DI"] = (abs(df["p_DI9"] - df["m_DI9"]) / (df["p_DI9"] + df["m_DI9"])).ewm(
      span=9, adjust=False, min_periods=9).mean().fillna(0)

  df["EMA10"] = df['close'].ewm(
      span=10, adjust=False, min_periods=10).mean().fillna(0)
  df["EMA12"] = df['close'].ewm(
      span=12, adjust=False, min_periods=12).mean().fillna(0)
  df["EMA24"] = df['close'].ewm(
      span=24, adjust=False, min_periods=24).mean().fillna(0)

  # расчет MACD
  df["MACD10"] = (df["EMA12"] - df["EMA24"]).ewm(
      span=10, adjust=False, min_periods=34).mean().fillna(0)

  df.index += 1

  # print(df.loc[52]["MACD10"])
  print(tabulate(df.loc[50:70], headers='keys', tablefmt='psql'))

  return round(np.quantile(df["volume"].values, 0.9999), 4), df["md_volume"].quantile(0.999), df


def test_ta_lib():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df = pd.read_sql_query(
      "SELECT open, high, low, close, volume FROM candles", cnx)

  ta_ADX = ADXIndicator(
      high=df["high"], low=df["low"], close=df["close"], window=9)

  df["ADX"] = ta_ADX.adx()
  df["ADX_pos"] = ta_ADX.adx_pos()
  df["ADX_neg"] = ta_ADX.adx_neg()

  print(tabulate(df.loc[50:70], headers='keys', tablefmt='psql'))
