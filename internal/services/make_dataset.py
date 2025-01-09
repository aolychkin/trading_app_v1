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
  df = df.groupby("pred").head(10000)

  # Преобразование в numpy.ndarray
  X = df_param.to_numpy()
  y = df_pred.to_numpy()
  target_names = ['class 0', 'class 1', 'class 2', 'class 3']

  # Разделение данных на обучающий и тестовый наборы
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42)

  # Масштабирование данных
  scaler = StandardScaler()
  X_train = scaler.fit_transform(X_train)
  X_test = scaler.transform(X_test)
  print("[УСПЕШНО] Масштабирование данных")

  # Создание модели SVM
  n_estimators = 10
  model = OneVsRestClassifier(BaggingClassifier(
      SVC(kernel='linear', C=1.0, random_state=42, verbose=1), max_samples=1.0 / n_estimators, n_estimators=n_estimators))
  print("[УСПЕШНО] Создание модели SVM")

  # Обучение модели
  model.fit(X_train, y_train)
  print("[УСПЕШНО] Обучение модели")

  # Предсказание классов для тестовых данных
  y_pred = model.predict(X_test)
  print("[УСПЕШНО] Предсказание классов для тестовых данных")

  # Оценка производительности модели
  accuracy = accuracy_score(y_test, y_pred)
  report = classification_report(
      y_test, y_pred, target_names=target_names)
  print("[УСПЕШНО] Оценка производительности модели")

  print(f"Accuracy: {accuracy}")
  print(report)

  joblib.dump(model, "model.pkl")

  # clf2 = joblib.load("model.pkl")
  # clf2.predict(X[0:1])

  # print(tabulate(df_param.loc[:10], headers='keys', tablefmt='psql'))
  # print(tabulate(df_pred.loc[:10], headers='keys', tablefmt='psql'))
  # print(tabulate(df.loc[:10], headers='keys', tablefmt='psql'))

  # print(df["pred"].value_counts())
