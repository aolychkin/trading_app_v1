from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator


# Утренняя торговая сессия: 04:00 – 7:00 utc.
s_morning = datetime(2024, 12, 2, 4, 00).strftime("%H:%M")
f_morning = datetime(2024, 12, 2, 7, 00).strftime("%H:%M")

# Основная торговая сессия: 7:00 – 16:00 utc.
s_main = datetime(2024, 12, 2, 7, 00).strftime("%H:%M")
f_main = datetime(2024, 12, 2, 15, 30).strftime("%H:%M")
# TODO: понять, что делать с последними 10 минутами графика, которые я могу предсказать, но не могу использовать
# В 15:40 начинается снятие заявок

# Дополнительная торговая сессия: 16:00 – 20:50 utc.
s_evening = datetime(2024, 12, 1, 16, 00).strftime("%H:%M")
f_evening = datetime(2024, 12, 3, 20, 50).strftime("%H:%M")


def w_session(candle_time, day):
  weekday = day.isoweekday()
  # 1–2 января, 7 января, 23 февраля, 8 марта, 1 мая, 9 мая, 12 июня, 4 ноября 2024 года
  s_h1 = datetime(day.year, 1, 1, 2, 00)
  f_h1 = datetime(day.year, 1, 3, 23, 59)

  s_h2 = datetime(day.year, 1, 6, 2, 00)
  f_h2 = datetime(day.year, 1, 8, 23, 59)

  s_h3 = datetime(day.year, 2, 22, 2, 00)
  f_h3 = datetime(day.year, 3, 24, 23, 59)

  s_h4 = datetime(day.year, 3, 7, 2, 00)
  f_h4 = datetime(day.year, 3, 9, 23, 59)

  s_h5 = datetime(day.year, 5, 1, 2, 00)
  f_h5 = datetime(day.year, 5, 2, 23, 59)

  s_h6 = datetime(day.year, 5, 8, 2, 00)
  f_h6 = datetime(day.year, 5, 10, 23, 59)

  s_h7 = datetime(day.year, 6, 11, 2, 00)
  f_h7 = datetime(day.year, 6, 13, 23, 59)

  s_h8 = datetime(day.year, 11, 3, 2, 00)
  f_h8 = datetime(day.year, 11, 5, 23, 59)

  # В какую торговую сессию торгуется свеча (what)
  if (weekday == 7) or (weekday == 6):
    return 3
  elif (s_h1 <= day <= f_h1) or (s_h2 <= day <= f_h2) or (s_h3 <= day <= f_h3) or (s_h4 <= day <= f_h4):
    return 3
  elif (s_h5 <= day <= f_h5) or (s_h6 <= day <= f_h6) or (s_h7 <= day <= f_h7) or (s_h8 <= day <= f_h8):
    return 3
  elif (s_morning < candle_time <= f_morning):
    return 0
  elif (s_evening < candle_time <= f_evening):
    return 2
  elif (s_main < candle_time <= f_main):
    return 1
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


def ta_ind():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')
  df = pd.read_sql_query(
      "SELECT open, high, low, close, volume FROM candles", cnx)
  df["md_volume"] = df["volume"].diff(
      periods=1).fillna(0)/df["volume"].shift(periods=1)

  ta_ADX = ADXIndicator(
      high=df["high"], low=df["low"], close=df["close"], window=9, fillna=True)
  print("Расчет ADX9 успешно завершен")

  ta_MACD = MACD(
      close=df["close"], window_fast=12, window_slow=24, window_sign=10, fillna=True)
  print("Расчет MACD10 успешно завершен")

  df["ADX9"] = ta_ADX.adx()
  df["ADX9_pos"] = ta_ADX.adx_pos()
  df["ADX9_neg"] = ta_ADX.adx_neg()
  print("ADX сохранен в df")

  df["EMA24"] = EMAIndicator(
      close=df["close"], window=24, fillna=True).ema_indicator()
  df["EMA100"] = EMAIndicator(
      close=df["close"], window=100, fillna=True).ema_indicator()
  df["EMA200"] = EMAIndicator(
      close=df["close"], window=200, fillna=True).ema_indicator()
  print("EMA сохранен в df")

  df["MACD10_signal"] = ta_MACD.macd_signal()
  df["MACD12_24"] = ta_MACD.macd()
  print("MACD сохранен в df")

  df["RSI9"] = RSIIndicator(close=df["close"], window=9, fillna=True).rsi()
  print("RSI сохранен в df")

  df["EMA24_volume"] = EMAIndicator(
      close=df["volume"], window=24, fillna=True).ema_indicator()
  df["EMA100_volume"] = EMAIndicator(
      close=df["volume"], window=100, fillna=True).ema_indicator()
  df["EMA200_volume"] = EMAIndicator(
      close=df["volume"], window=200, fillna=True).ema_indicator()
  print("EMA VOLUME сохранен в df")

  df.index += 1  # синхранизируем с id бд
  print(tabulate(df.loc[235765:235780], headers='keys', tablefmt='psql'))

  return round(np.quantile(df["volume"].values, 0.9999), 4), df["md_volume"].quantile(0.9999), df
