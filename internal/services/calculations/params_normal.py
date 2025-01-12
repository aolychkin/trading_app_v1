from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import internal.lib.calculations.pn_helper as pnhelp
import internal.domain.models as models

# TODO: проверить - под сомнением
if __name__ == '__main__':
  df = pnhelp.prepare_data()

  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    for index, row in tqdm(df.iterrows()):
      data = models.Params_normal(
          candle_id=row["candle_id"],

          hl_C=row["hl_C"],
          MACD10=row["MACD10"],
          сEMA24=row["сEMA24"],
          RSI9=row["RSI9"],
          ADX9=row["ADX9"],
          DI9=row["DI9"],

          vEMA24=row["vEMA24"],
      )
      session.add(data)
    session.commit()
