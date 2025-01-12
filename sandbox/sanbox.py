from tabulate import tabulate
from datetime import datetime

import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# float dot[2];  // точка пересечения

def cross(s_MACD, f_MACD, s_signal, f_signal):
  y1 = 1
  y2 = 2
  y3 = 1
  y4 = 2
  n = 0
  is_cross = 0
  down_up = -1
  if (y2 - y1 != 0):
    q = (f_MACD - s_MACD) / (y1 - y2)
    sn = (s_signal - f_signal) + (y3 - y4) * q
    if (not sn):
      return 0
    fn = (s_signal - s_MACD) + (y3 - y1) * q
    n = fn / sn
  else:
    n = (y3 - y1) / (y3 - y4)

  dot1 = s_signal + (f_signal - s_signal) * n
  dot2 = y3 + (y4 - y3) * n
  if (1 <= dot2 <= 2):
    is_cross = 1
    if (dot2 == 2):
      down_up = 1 if (s_MACD/s_signal-1 < 0) else 0
    elif (dot2 == 1):
      down_up = 1 if (f_MACD/f_signal-1 > 0) else 0
    else:
      down_up = 1 if (s_MACD/s_signal-1 < 0) else 0
  else:
    is_cross = 0

  power_rate = np.abs(np.mean([s_MACD, f_MACD]) / np.mean([s_signal, f_signal]) - 1)
  if down_up == 1:
    power = power_rate
  elif down_up == 0:
    power = -power_rate
  else:
    power = power_rate  # TODO: деленный или умноженный на кол-во свечей от сигнала

  return is_cross, down_up, power, dot1, dot2


if __name__ == '__main__':
  # is_cross, down_up, power, dot1, dot2 = cross(16, 19, 17, 16)
  # is_cross, down_up, power, dot1, dot2 = cross(21, 20, 19, 20)
  # is_cross, down_up, power, dot1, dot2 = cross(19, 23, 16, 16)
  # is_cross, down_up, power, dot1, dot2 = cross(-0.0219071, -0.0276644, 0.0246507, -0.0535724)
  # is_cross, down_up, power, dot1, dot2 = cross(-0.0245294,     -0.0346309,      -0.0104221, -0.0800876)
  is_cross, down_up, power, dot1, dot2 = cross(60, 80, 70, 70)
  if (is_cross):
    if down_up == 1:
      print("Пересекает снизу вверх")
      print(f"Сила: {power}")
    else:
      print("Пересекает сверху вниз")
      print(f"Сила: {power}")
    print(dot1, dot2)
  else:
    print("Not cross!")
    print(f"Сила: {power}")
    print(dot1, dot2)

# print(tabulate(X.loc[:10], headers='keys', tablefmt='psql'))
