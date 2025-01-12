from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import internal.lib.calculations.params_helpers as phelp
import internal.domain.models as models

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  macd = phelp.macd()
  rsi = phelp.rsi()
  adx = phelp.adx()

  with Session(engine) as session:
    for ind in tqdm(session.query(models.Indicators).filter(models.Indicators.session == 1)):
      if ind.id < 2:
        continue

      # ind_p = session.get(models.Indicators, ind.id-1)
      data = models.Params(
          candle_id=ind.candle_id,

          hl_C=ind.high/ind.low-1,
          MACD10=macd.loc[ind.id],  # Из гугл таблицы: пересечение и сила
          сEMA24=ind.close / ind.EMA24 - 1,  # Просто Close выше или ниже EMA24
          RSI9=rsi.loc[ind.id],  # Сигналом является только: Выход из "зоны" комфорта
          ADX9=adx.loc[ind.id],  # Растущий и высокий тренд (больше 25 и чем больше - тем лучше) = подтверждение продажи и покупки. "Для ADX все что не рост - все слабость тренда"
          DI9=ind.ADX9_pos / ind.ADX9_neg - 1,

          vEMA24=ind.volume / ind.EMA24_volume - 1,
      )

      if ind.id == 51:
        pp(data.__dict__)
      session.add(data)
    session.commit()
