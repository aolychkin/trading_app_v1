from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import internal.lib.indicators_helper as ihelp
import internal.domain.models as models

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    # валидные данные в df только с id = 50
    max_volume, max_md_volume, df = ihelp.ta_ind()

    for candle in tqdm(session.query(models.Candles).all()):
      if candle.id < 51:
        continue

      data = models.Indicators(
          candle_id=candle.id,

          # индикторы группы: time
          weekday=candle.time.isoweekday(),
          session=ihelp.w_session(candle.time.strftime("%H:%M")),
          session_len=540,
          s_min=ihelp.w_s_min(candle.time.strftime("%H:%M")),

          open=candle.open,
          high=candle.high,
          low=candle.low,
          close=candle.close,
          ADX9=df.loc[candle.id]["ADX9"],
          ADX9_pos=df.loc[candle.id]["ADX9_pos"],
          ADX9_neg=df.loc[candle.id]["ADX9_neg"],
          EMA24=df.loc[candle.id]["EMA24"],
          MACD10_signal=df.loc[candle.id]["MACD10_signal"],
          MACD12_24=df.loc[candle.id]["MACD12_24"],
          RSI9=df.loc[candle.id]["RSI9"],

          max_volume=max_volume,
          volume=candle.volume,
          md_volume=max_md_volume,
      )

      if candle.id == 51:
        pp(data.__dict__)
      session.add(data)
    session.commit()
