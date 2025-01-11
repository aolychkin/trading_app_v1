from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import internal.lib.calculations.pn_helper as pnhelp
import internal.domain.models as models


if __name__ == '__main__':
  df = pnhelp.prepare_data()

  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    for index, row in tqdm(df.iterrows()):
      data = models.Params_normal(
          candle_id=row["candle_id"],

          wday_C=row["wday_C"],
          s_min_C=row["s_min_C"],

          co_C=row["co_C"],
          hl_C=row["hl_C"],
          hc_CP=row["hc_CP"],

          MACD10_P=row["MACD10_P"],
          MACD10_C=row["MACD10_C"],
          сEMA24_C=row["сEMA24_C"],
          сEMA24_P=row["сEMA24_P"],
          cEMA_100_C=row["cEMA_100_C"],
          cEMA_100_P=row["cEMA_100_P"],
          cEMA_200_C=row["cEMA_200_C"],
          cEMA_200_P=row["cEMA_200_P"],
          RSI9_C=row["RSI9_C"],
          RSI9_P=row["RSI9_P"],
          ADX9_C=row["ADX9_C"],
          ADX9_P=row["ADX9_P"],
          DI9_C=row["DI9_C"],
          DI9_P=row["DI9_P"],

          vEMA24_C=row["vEMA24_C"],
          vEMA24_P=row["vEMA24_P"],
          vEMA100_C=row["vEMA100_C"],
          vEMA100_P=row["vEMA100_P"],
          vEMA200_C=row["vEMA200_C"],
          vEMA200_P=row["vEMA200_P"],
          s_vol_C=row["s_vol_C"],
          d_vol_CP=row["d_vol_CP"],
      )
      session.add(data)
    session.commit()

  # ind_p = session.get(models.Indicators, ind.id-1)
  #   data = models.Params(
  #       candle_id=ind.candle_id,

  #       wday_C=(ind.weekday / 3.5) - 1,
  #       s_min_C=(ind.s_min / (ind.session_len / 2)) - 1,

  #       co_C=(ind.close / ind.open) - 1,
  #       hl_C=(ind.high / ind.low)-1,  # УБРАТЬ ИНДИКАТОР
  #       hc_CP=(ind.high / ind_p.close)-1,

  #       MACD10_C=(ind.MACD10_signal/ind.MACD12_24)-1,
  #       MACD10_P=(ind_p.MACD10_signal/ind_p.MACD12_24)-1,
  #       сEMA24_C=(ind.close / ind.EMA24) - 1,
  #       сEMA24_P=(ind_p.close / ind_p.EMA24) - 1,
  #       cEMA_100_C=(ind.close / ind.EMA100) - 1,
  #       cEMA_100_P=(ind_p.close / ind_p.EMA100) - 1,
  #       cEMA_200_C=(ind.close / ind.EMA200) - 1,
  #       cEMA_200_P=(ind_p.close / ind_p.EMA100) - 1,
  #       RSI9_C=ind.RSI9,
  #       RSI9_P=ind_p.RSI9,
  #       ADX9_C=ind.ADX9,
  #       ADX9_P=ind_p.ADX9,
  #       DI9_C=(ind.ADX9_pos/ind.ADX9_neg)-1,
  #       DI9_P=(ind_p.ADX9_pos/ind_p.ADX9_neg)-1,

  #       vEMA24_C=(ind.volume / ind.EMA24) - 1,
  #       vEMA24_P=(ind_p.volume / ind_p.EMA24) - 1,
  #       vEMA100_C=(ind.volume / ind.EMA100) - 1,
  #       vEMA100_P=(ind_p.volume / ind_p.EMA100) - 1,
  #       vEMA200_C=(ind.volume / ind.EMA200) - 1,
  #       vEMA200_P=(ind_p.volume / ind_p.EMA200) - 1,
  #       s_vol_C=(ind.volume / ind.max_volume)-1,
  #       d_vol_CP=(ind.volume / ind_p.volume / ind.md_volume)-1,
  #   )

  #   if ind.id == 51:
  #     pp(data.__dict__)
  #   session.add(data)
  # session.commit()
