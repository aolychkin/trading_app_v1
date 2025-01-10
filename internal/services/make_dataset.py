from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np
from adjdatatools.preprocessing import AdjustedScaler
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score

import internal.lib.ml_helper as mlrhelp


if __name__ == '__main__':
  # Загрузка данных
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df_param = pd.read_sql_query(
      "SELECT * from params", cnx)
  df_param.drop(columns=["id", "candle_id"], inplace=True)

  df_pred = pd.read_sql_query(
      "SELECT * from predictions", cnx)
  df_pred.drop(columns=["id", "candle_id"], inplace=True)

  df = df_param
  df["pred"] = df_pred["high_10min"]
  df = df.groupby("pred").head(13300)

  df_param = df.drop(columns=["pred"])
  df_pred = df["pred"]

  # Подготовка данных
  X_train, X_test, y_train, y_test = mlrhelp.prepare_data(df_param, df_pred)

  # Создание и обучение модели SVC
  model = mlrhelp.create_model_SVC("fast", X_train, y_train)

  # # Создание и обучение модели дерева решений
  # model = mlrhelp.create_model_TREE("", X_train, y_train)

  # Оценка производительности модели
  mlrhelp.model_score(model, X_test, y_test)

  # Сохранение модели
  joblib.dump(model, "./model/model_10m_v3.pkl")  # 0.58

  # Загрузка модели потом
  # clf2 = joblib.load("model.pkl")
  # clf2.predict(X[0:1])

  # print(tabulate(df_param.loc[:10], headers='keys', tablefmt='psql'))
  # print(df_pred.loc[:10])
  # print(tabulate(df.loc[:10], headers='keys', tablefmt='psql'))

  # print(df["pred"].value_counts())
