from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score


def prepare_data(df_param, df_pred):  # Подготовка набора данных
  # Преобразование Pandas в numpy.ndarray
  X = df_param.to_numpy()
  y = df_pred.to_numpy()

  # Разделение данных на обучающий и тестовый наборы
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42)

  # Масштабирование данных
  scaler = StandardScaler()
  X_train = scaler.fit_transform(X_train)
  X_test = scaler.transform(X_test)

  print("[УСПЕШНО] Данные успешно подготовлены")

  return X_train, X_test, y_train, y_test


def create_model_SVC(type: str, X_train, y_train):  # Создание модели SVM
  if type == "fast":
    # Если нужно расчитать параллельно
    #  class_weight="balanced"
    n_estimators = 10
    model = OneVsRestClassifier(BaggingClassifier(
        SVC(kernel='rbf', C=1000.0, random_state=42, verbose=1), max_samples=1.0 / n_estimators, n_estimators=n_estimators, random_state=42))
    model.fit(X_train, y_train)  # Обучение модели
    return model
  elif type == "detect":
    # Если нужно определить наилучшее ядро
    model = SVC(random_state=42, verbose=1)
    param_grid = {'C': [0.1, 1, 10, 100], 'kernel': ['linear', 'rbf']}
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)  # Поиск лучших параметров модели
    print("Лучшие параметры: {}".format(grid_search.best_params_))
    return grid_search
  else:
    model = SVC(kernel='rbf', C=100, random_state=42, verbose=1)
    model.fit(X_train, y_train)  # Обучение модели
    return model

  # Лучшие параметры: {'C': 100, 'kernel': 'rbf'}


def model_score(model, X_test, y_test):  # Оценка производительности модели
  # Предсказание классов для тестовых данных
  y_pred = model.predict(X_test)

  # Оценка производительности модели
  target_names = ['class 0', 'class 1', 'class 2']
  accuracy = accuracy_score(y_test, y_pred)
  report = classification_report(y_test, y_pred, target_names=target_names)

  print(f"Accuracy: {accuracy}")
  print(report)
