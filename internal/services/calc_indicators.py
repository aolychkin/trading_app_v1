from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import domain.models as models
import internal.lib.indicators_helper as ihelp

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    ihelp.test_ta_lib()
    # # валидные данные в df только с id = 50
    # max_volume, max_md_volume, df = ihelp.w_all_ema()

    # for candle in tqdm(session.query(models.Candles).all()):
    #   if candle.id < 51:
    #     continue

    #   candle_p = session.get(models.Candles, candle.id-1)
    #   data = models.Indicators(
    #       candle_id=candle.id,

    #       # индикторы группы: time
    #       weekday=candle.time.isoweekday(),
    #       session=ihelp.w_session(candle.time.strftime("%H:%M")),
    #       session_len=540,
    #       s_min=ihelp.w_s_min(candle.time.strftime("%H:%M")),

    #       # индикторы группы: open, high, low
    #       open_C=candle.open,
    #       open_P=candle_p.open,
    #       high_C=candle.high,
    #       high_P=candle_p.high,
    #       low_C=candle.low,
    #       low_P=candle_p.low,
    #       close_C=candle.close,
    #       close_P=candle_p.close,
    #       p_DM=Decimal(df.loc[candle.id]["p_DM"]),
    #       m_DM=Decimal(df.loc[candle.id]["m_DM"]),

    #       # индикторы группы: close
    #       TR=Decimal(df.loc[candle.id]["TR"]),
    #       p_DI9=Decimal(df.loc[candle.id]["p_DI9"]),
    #       m_DI9=Decimal(df.loc[candle.id]["m_DI9"]),
    #       EMA9=Decimal(df.loc[candle.id]["EMA9"]),
    #       EMA9_GAIN=Decimal(df.loc[candle.id]["EMA9_GAIN"]),
    #       EMA9_LOSS=Decimal(df.loc[candle.id]["EMA9_LOSS"]),
    #       EMA9_ABS_DI=Decimal(df.loc[candle.id]["EMA9_ABS_DI"]),
    #       EMA10_C=Decimal(df.loc[candle.id]["EMA10"]),
    #       EMA10_P=Decimal(df.loc[candle.id-1]["EMA10"]),
    #       EMA12_C=Decimal(df.loc[candle.id]["EMA12"]),
    #       EMA12_P=Decimal(df.loc[candle.id-1]["EMA12"]),
    #       EMA24_C=Decimal(df.loc[candle.id]["EMA24"]),
    #       EMA24_P=Decimal(df.loc[candle.id-1]["EMA24"]),
    #       MACD10_С=Decimal(df.loc[candle.id]["MACD10"]),
    #       MACD10_P=Decimal(df.loc[candle.id-1]["MACD10"]),

    #       # индикторы группы: volume
    #       max_volume=max_volume,
    #       volume_C=candle.volume,
    #       volume_P=candle_p.volume,
    #       md_volume=Decimal(max_md_volume)
    #   )

    #   if candle.id == 51:
    #     pp(data.__dict__)
    #   session.add(data)
    # session.commit()
