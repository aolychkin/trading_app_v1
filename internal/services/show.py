from datetime import datetime
from tabulate import tabulate
from tqdm import tqdm
from pprint import pp

import sqlite3
import pandas as pd
import joblib
import plotly.graph_objects as go
import numpy as np

import internal.lib.show_helpers as shelp


if __name__ == '__main__':
  # Загрузка данных
  df_model, X = shelp.get_data()

  model = joblib.load("./model/model_10m_v3.pkl")

  for index, x in enumerate(X):
    df_model.loc[index, ["minus", "p_0.2", "p_0.5"]] = (
        model.predict_proba(x.reshape(1, -1))).ravel()
  print(tabulate(df_model.head(), headers='keys', tablefmt='psql'))

  # # TODO: нормализовать прямо в бд

  # fig = go.Figure(data=[go.Candlestick(x=df['time'],
  #                 open=df['open'],
  #                 high=df['high'],
  #                 low=df['low'],
  #                 close=df['close'])])
# fig.add_trace(go.Scatter(
  #     x=[row["time"]],
  #     y=[df.loc[index]['close']],
  #     mode='markers',
  #     name='markers')
  # )

  # shelp.strategy(
  #     df_model, accuracy=0.9, stop_loss=0.004, take_profit=0.003)  # +1
  # shelp.strategy(
  #     df_model, accuracy=0.9, stop_loss=0.005, take_profit=0.005)  # +1
  # shelp.strategy(
  #     df_model, accuracy=0.91, stop_loss=0.005, take_profit=0.005)
  # shelp.strategy(
  #     df_model, accuracy=0.91, stop_loss=0.004, take_profit=0.003)  # +1

# ____
  shelp.strategy(
      df_model, accuracy=0.9, stop_loss=0.003, take_profit=0.0025)
  # shelp.strategy(
  #     df_model, accuracy=0.9, stop_loss=0.002, take_profit=0.002)  # +1
  # shelp.strategy(
  #     df_model, accuracy=0.9, stop_loss=0.004, take_profit=0.003)  # +1
# ____

  # shelp.strategy(
  #     df_model, accuracy=0.9, stop_loss=0.002, take_profit=0.003)
