from datetime import datetime
from decimal import Decimal

from pprint import pp
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import internal.lib.calculations.predictions_helper as prhelp
import internal.domain.models as models

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    df = prhelp.w_max_10min()

    for param in tqdm(session.query(models.Params).all()):

      data = models.Predictions(
          candle_id=param.candle_id,
          high_10min=df.loc[param.candle_id]["pred_class"]
      )

      if param.id == 51:
        pp(data.__dict__)
      session.add(data)
    session.commit()
