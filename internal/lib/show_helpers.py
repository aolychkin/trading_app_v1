from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm
from pprint import pp

import sqlite3
import pandas as pd
import joblib
import plotly.graph_objects as go
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report


import internal.lib.calculations.predictions_helper as prhelp
import internal.domain.models as models


def get_data():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df = pd.read_sql_query(
      "SELECT * from candles where time >= '2024-12-20 07:01:00.000' and time <= '2024-12-20 15:30:00.00'", cnx)
  # "SELECT * from candles where time >= '2024-12-20 07:01:00.000' and time <= '2024-12-20 15:30:00.00'", cnx)
  # "SELECT * from candles where time >= '2024-12-18 07:01:00.000' and time <= '2024-12-18 15:30:00.00'", cnx)

  max_id = df["id"].max()
  min_id = df["id"].min()

  data = pd.read_sql_query(
      "SELECT * from params where candle_id >= (?) and candle_id <= (?)", cnx, params=(str(min_id), str(max_id)))

  data.drop(columns=["id", "candle_id"], inplace=True)

  # Fit data
  scaler = fit_data()

  # Подготовка данных
  X = data.to_numpy()
  X_prod = scaler.transform(X)

  # print(tabulate(data.head(), headers='keys', tablefmt='psql'))
  # print(max_id, min_id)

  print("\n[УСПЕШНО] Данные успешно получены")
  return df, X_prod


def fit_data():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  scaler = StandardScaler()
  df_param = pd.read_sql_query(
      "SELECT * from params", cnx)
  df_param.drop(columns=["id", "candle_id"], inplace=True)
  # print(tabulate(df_param.head(), headers='keys', tablefmt='psql'))
  X_to_fit = df_param.to_numpy()
  X_to_fit = scaler.fit_transform(X_to_fit)

  return scaler


def strategy(data, accuracy, stop_loss, take_profit, wait=10, debug=False):
  indx = 0
  profile = pd.DataFrame()
  transaction_id = 0
  profile["id"] = [transaction_id]
  profile["transaction"] = [700]
  profile["balance"] = [700]
  profile["candle_id"] = [0]
  profile["price"] = [700]
  profile["is_closed"] = [1]
  profile["cause"] = ["money"]
  profile["accuracy"] = [0.00]
  profile["result"] = [""]

  m_count = 0
  p_count = 0
  count = 0

  # TODO: Если больше N открытых сделок - больше не открываю
  # TODO: Подкрепить показателями теми же самыми за период в 10 минут для каждой свечи минутной внутри (более длинный тренд)
  # TODO: Обучение норм, нужно работать с данными

  for index, row in tqdm(data.iterrows()):
    # Сигнал на покупку акции
    if (row["target"] >= accuracy) and (profile[profile["is_closed"] == 0]["is_closed"].count() < 4):
      transaction_id += 1
      buy = round(row['close'] * (1+0.0004), 2)  # TODO: увеличить точность. Price без комиссии
      balance = round(profile.loc[indx, "balance"], 2)
      indx += 1
      profile.loc[indx, "id"] = transaction_id
      profile.loc[indx, "transaction"] = -buy
      profile.loc[indx, "balance"] = round(balance-buy, 2)
      profile.loc[indx, "candle_id"] = row["id"]
      profile.loc[indx, "price"] = buy
      profile.loc[indx, "is_closed"] = 0
      profile.loc[indx, "accuracy"] = row["target"]

    for index, p_row in profile.iterrows():
      if (0 < row["id"] - p_row["candle_id"] <= wait) and (p_row["is_closed"] == 0):
        if (row["high"]/p_row["price"] - 1 >= take_profit):
          indx += 1
          sell = round(row['high'] * (1-0.0004), 2)
          profile.loc[indx, "id"] = p_row["id"]
          profile.loc[indx, "transaction"] = sell
          profile.loc[indx, "balance"] = round(profile.loc[indx-1, "balance"]+sell, 2)
          profile.loc[indx, "candle_id"] = row["id"]
          profile.loc[indx, "price"] = sell
          profile.loc[indx, "is_closed"] = 1
          profile.loc[index, "is_closed"] = 1
          profile.loc[indx, "cause"] = "take_profit"
          profile.loc[index, "cause"] = "take_profit"
          profile.loc[index, "result"] = "+"
        elif (row["low"]/p_row["price"] - 1 <= -stop_loss):
          indx += 1
          sell = round(row['low'] * (1+0.0004), 2)
          profile.loc[indx, "id"] = p_row["id"]
          profile.loc[indx, "transaction"] = sell
          profile.loc[indx, "balance"] = round(profile.loc[indx-1, "balance"]+sell, 2)
          profile.loc[indx, "candle_id"] = row["id"]
          profile.loc[indx, "price"] = sell
          profile.loc[indx, "is_closed"] = 1
          profile.loc[index, "is_closed"] = 1
          profile.loc[indx, "cause"] = "stop_loss"
          profile.loc[index, "cause"] = "stop_loss"
          profile.loc[index, "result"] = "-"
      elif (row["id"] - p_row["candle_id"] > 10) and (p_row["is_closed"] == 0):
        indx += 1
        sell = round(row['low'] * (1+0.0004), 2)
        profile.loc[indx, "id"] = p_row["id"]
        profile.loc[indx, "transaction"] = sell
        profile.loc[indx, "balance"] = round(profile.loc[indx-1, "balance"]+sell, 2)
        profile.loc[indx, "candle_id"] = row["id"]
        profile.loc[indx, "price"] = sell
        profile.loc[indx, "is_closed"] = 1
        profile.loc[index, "is_closed"] = 1
        profile.loc[indx, "cause"] = "expired"
        profile.loc[index, "cause"] = "expired"
        if (profile.loc[indx, "price"] / profile.loc[index, "price"] - 1 > 0):
          profile.loc[index, "result"] = "+"
        elif (profile.loc[indx, "price"] / profile.loc[index, "price"] - 1 == 0):
          profile.loc[index, "result"] = "="
        else:
          profile.loc[index, "result"] = "-"

  delta_money = round((profile.tail(1)["balance"].values[0] / profile.head(1)["balance"].values[0] - 1)*100, 2)
  stop_order = profile["cause"].value_counts().sort_index().values
  profit = profile["result"].value_counts().sort_index().values
  print(f"\
    Параметры: acc={accuracy}, sl={stop_loss}, tp={take_profit} \n \
    Итоговый баланс: {profile.tail(1)["balance"].values[0]} \n \
    Рост баланса: {"+" if delta_money > 0 else ""}{delta_money}% \n \
    Всего сделок: {np.floor(profile[profile["is_closed"] == 1]["is_closed"].count() / 2)} \n \
    Соотношение сделок (+/-): {round(profit[1]/profit[2], 2)} \n \
    take_profit: {stop_order[3]/2}  | |  stop_loss: {stop_order[2]/2}  | |  expired: {stop_order[0]/2}\n")

  if (debug):
    profile.to_csv('out.csv', index=False)
    print(tabulate(profile.head(10), headers='keys', tablefmt='psql'))
    print(profile["is_closed"].value_counts())
    print(profile["result"].value_counts().sort_index())
    print(profile["cause"].value_counts().sort_index())
    print(profile["balance"].min())
