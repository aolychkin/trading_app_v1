from tabulate import tabulate
from datetime import datetime

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


dat = datetime(2024, 12, 3, 20, 50)
print(dat.year)

# print(tabulate(X.loc[:10], headers='keys', tablefmt='psql'))
