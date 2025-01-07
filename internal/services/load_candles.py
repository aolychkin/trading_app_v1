from datetime import datetime
from calendar import monthrange

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import pandas as pd
from tqdm import tqdm
from tabulate import tabulate

from tinkoff.invest import Client, CandleInterval
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX

import internal.domain.models as models

TOKEN = 't.fDimiyDvouBZCRipO5XsUUDuWDv8rRAJwWAZkjytq0KLLwxTKBld4HEXkpE0kC8TrL_Bo1WuValllzW2I-5ddg'
FIGI = 'BBG004S68CP5'

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  with Session(engine) as session:
    with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
      for index, month in tqdm(enumerate(range(1, 13))):
        for day in tqdm(range(monthrange(2024, month)[1])):
          for candle in client.market_data.get_candles(
                  figi=FIGI,
                  from_=datetime(2024, month, day+1, 6, 0),
                  # (2024, 10, 31, 23, 59)
                  to=datetime(2024, month, day+1, 23, 59),
                  interval=CandleInterval.CANDLE_INTERVAL_1_MIN).candles:

            data = models.Candles(
                figi=FIGI,
                open=candle.open.units + candle.open.nano / 1000000000,
                high=candle.high.units + candle.high.nano / 1000000000,
                low=candle.low.units + candle.low.nano / 1000000000,
                close=candle.close.units + candle.close.nano / 1000000000,
                volume=candle.volume,
                time=candle.time,
                is_complete=candle.is_complete
            )
            session.add(data)
      session.commit()
