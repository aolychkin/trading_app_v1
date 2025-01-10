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


import internal.lib.predictions_helper as prhelp
import internal.domain.models as models


def get_data():
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df = pd.read_sql_query(
      "SELECT * from candles where time >= '2024-12-19 07:01:00.000' and time <= '2024-12-19 15:30:00.00'", cnx)

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


def strategy(data, accuracy, stop_loss, take_profit):
  start_balance = 700
  balance_df = pd.DataFrame(columns=['transaction'])
  indx = 0
  m_count = 0
  p_count = 0
  count = 0
  balance_df["transaction"] = [start_balance]
  for index, row in data.iterrows():
    # fig.add_trace(go.Scatter(
    #     x=[row["time"]],
    #     y=[df.loc[index]['close']],
    #     mode='markers',
    #     name='markers')
    # )
    flag = 0
    if row["p_0.5"] >= accuracy:
      balance_df.loc[len(balance_df)] = -data.loc[index]['close'] * (1+0.0004)
      count += 1
      for i in range(10):
        if (data.loc[index+i+1]['high'] / data.loc[index]['close'] - 1) >= take_profit:
          balance_df.loc[len(balance_df)] = (
              data.loc[index+i+1]['high'] * (1-0.0004))
          flag = 1
          p_count += 1
          break
        elif (data.loc[index+i+1]['low'] / data.loc[index]['close'] - 1) <= -stop_loss:
          balance_df.loc[len(balance_df)] = (
              data.loc[index+i+1]['low'] * (1-0.0004))
          flag = 1
          m_count += 1
          break
      if flag == 0:
        balance_df.loc[len(balance_df)] = (
            data.loc[index+1+9]['low'] * (1-0.0004))
        m_count += 1

  balance_df.to_csv('out.csv', index=False)
  print(f"\
    Параметры: acc={accuracy}, sl={stop_loss}, tp={take_profit} \
    Итоговый баланс: {round(balance_df['transaction'].sum(), 2)} \n \
    Рост баланса: +{round((balance_df['transaction'].sum()/start_balance-1)*100, 2)}% \n \
    Всего сделок: {count} \n \
    Соотношение сделок (+/-): {round(p_count/m_count, 2)} \n \
    Сделок: в плюс: {p_count} \t в минус: {m_count} \n")

  # except:
  #   balance_df.loc[len(balance_df)] = -(
  #       balance_df.loc[len(balance_df)-1]['transaction'] * 0.998)
  #   m_count += 1
  #   print("WARN")
