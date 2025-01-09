from tabulate import tabulate

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Загрузка данных
iris = load_iris()
X = iris.data
y = iris.target

print(iris.target_names)
print(y[0:10])

# print(tabulate(X.loc[:10], headers='keys', tablefmt='psql'))
