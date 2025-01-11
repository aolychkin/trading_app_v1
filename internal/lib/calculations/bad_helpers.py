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


def create_model_TREE(type: str, X_train, y_train):  # Создание модели SVM
  if type == "fast":
    n_estimators = 10
    model = BaggingClassifier(
        DecisionTreeClassifier(max_depth=9, max_features=16, random_state=42), max_samples=1.0 / n_estimators, n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)  # Обучение модели
    return model
  elif type == "detect":
    # Если нужно определить наилучшее ядро
    tree_params = {'max_depth': range(1, 11), 'max_features': range(4, 19)}
    model = DecisionTreeClassifier(random_state=42)  # random_state=17

    grid_search = GridSearchCV(
        model, tree_params, cv=5, n_jobs=-1, verbose=True)
    grid_search.fit(X_train, y_train)

    print("Лучшие параметры: {}".format(grid_search.best_params_))
    print("Лучшие показатели: {}".format(grid_search.best_score_))

    return grid_search
  else:
    n_estimators = 10
    model = DecisionTreeClassifier(
        max_depth=9, max_features=16, random_state=42)
    model.fit(X_train, y_train)  # Обучение модели
    return model

  # Лучшие параметры: {'max_depth': 9, 'max_features': 16}
  # Лучшие показатели: 0.6031015037593985


def create_model_RFC(type: str, X_train, y_train):  # Создание модели SVM
  if type == "fast":
    pass
  elif type == "detect":
    # Если нужно определить наилучшее ядро
    model = RandomForestClassifier(
        n_estimators=100, n_jobs=-1, random_state=42, verbose=1)
    param_grid = {'max_depth': range(1, 11), 'max_features': range(4, 19)}

    grid_search = GridSearchCV(
        model, param_grid, cv=5, n_jobs=-1, verbose=True)
    grid_search.fit(X_train, y_train)

    print("Лучшие параметры: {}".format(grid_search.best_params_))
    print("Лучшие показатели: {}".format(grid_search.best_score_))

    return grid_search
  else:
    pass

  # Лучшие параметры: {'max_depth': 9, 'max_features': 16}
  # Лучшие показатели: 0.6031015037593985
