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
  df_param, df_pred = mlrhelp.get_data()

  # Подготовка данных
  X_train, X_test, y_train, y_test = mlrhelp.prepare_data(df_param, df_pred)

  # Создание и обучение модели SVC
  model = mlrhelp.create_model_SVC("fast", X_train, y_train)

  # Создание и обучение модели дерева решений
#   model = mlrhelp.create_model_TREE("", X_train, y_train)

  # Оценка производительности модели
  mlrhelp.model_score(model, X_test, y_test)

  # Сохранение модели
  joblib.dump(model, "./model_v2/model_1.pkl")  # 0.58 # 0.45

# ____ DRAFT ____
# Загрузка модели потом
# clf2 = joblib.load("model.pkl")
# clf2.predict(X[0:1])

# print(tabulate(df_param.loc[:10], headers='keys', tablefmt='psql'))
# print(df_pred.loc[:10])
# print(tabulate(df.loc[:10], headers='keys', tablefmt='psql'))

# print(df["pred"].value_counts())
