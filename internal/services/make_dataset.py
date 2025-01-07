from datetime import datetime
from tabulate import tabulate

import sqlite3
import pandas as pd
import numpy as np

if __name__ == '__main__':
  cnx = sqlite3.connect('./storage/sqlite/shares.db')  # TODO: close context
  df = pd.read_sql_query(
      "SELECT * from params", cnx)
  df.drop(columns=['id', 'candle_id'], inplace=True)

  print(tabulate(df.loc[:10], headers='keys', tablefmt='psql'))
