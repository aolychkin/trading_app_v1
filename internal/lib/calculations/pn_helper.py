from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MaxAbsScaler, RobustScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score
from adjdatatools.preprocessing import AdjustedScaler


def prepare_data(scaler="abs", debug=True):  # Подготовка набора данных
  # Загрузка данных
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df_param = pd.read_sql_query(
      "SELECT * from params", cnx)
  df_param.drop(columns=["id"], inplace=True)  # "candle_id"

  cols = df_param.columns.values[3:]
  Q1 = df_param[cols].quantile(0.05)
  Q3 = df_param[cols].quantile(0.95)
  IQR = Q3 - Q1
  df_param = df_param[~((df_param[cols] < (Q1 - 1.5 * IQR)) | (df_param[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
  # print(df_param["candle_id"].count())
  # print(df_param["co_C"].count())
  # print(tabulate(df_param.iloc[:20, :8], headers='keys', tablefmt='psql'))

  # Масштабирование данных
  if scaler == "standard":
    scaler = StandardScaler()
  else:
    scaler = MaxAbsScaler()
  cols = df_param.columns.values[1:]
  x_scaled = scaler.fit_transform(df_param[cols].to_numpy())
  df = pd.DataFrame(data=x_scaled.reshape(df_param["co_C"].count(), -1), columns=df_param[cols].columns)
  df.insert(loc=0, column='candle_id', value=df_param[df_param.columns.values[0:1]].values)
  # print(df_param[df_param.columns.values[:1]].count())
  # print(df[df_param.columns.values[:1]].count())

  if debug:
    print(tabulate(df.iloc[:6, :8], headers='keys', tablefmt='psql'))
    print(df["co_C"].max())
    print(df["MACD10_C"].max())

  # print(df["candle_id"].count())
  # print(df["co_C"].count())
  return df
