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
    for ind in tqdm(session.query(models.Indicators).filter(models.Indicators.session == 1)):
      if ind.id < 2:
        continue

      ind_p = session.get(models.Indicators, ind.id-1)
      data = models.Params(
          candle_id=ind.candle_id,

          wday_C=(ind.weekday / 3.5) - 1,
          s_min_C=(ind.s_min / (ind.session_len / 2)) - 1,

          co_C=(ind.close / ind.open) - 1,
          hl_C=(ind.high / ind.low)-1,  # УБРАТЬ ИНДИКАТОР
          hc_CP=(ind.high / ind_p.close)-1,

          MACD10_C=(ind.MACD10_signal/ind.MACD12_24)-1,
          MACD10_P=(ind_p.MACD10_signal/ind_p.MACD12_24)-1,
          сEMA24_C=(ind.close - ind.EMA24) - 1,
          сEMA24_P=(ind_p.close - ind_p.EMA24) - 1,
          RSI9_C=(ind.RSI9/50)-1,
          RSI9_P=(ind_p.RSI9/50)-1,
          ADX9_C=(ind.ADX9/50)-1,
          ADX9_P=(ind_p.ADX9/50)-1,
          DI9_C=(ind.ADX9_pos/ind.ADX9_neg)-1,
          DI9_P=(ind_p.ADX9_pos/ind_p.ADX9_neg)-1,

          s_vol_C=(ind.volume / (ind.max_volume / 2))-1,
          d_vol_CP=(ind.volume / ind_p.volume / (ind.md_volume/2))-1,
      )

      if ind.id == 51:
        pp(data.__dict__)
      session.add(data)
    session.commit()
