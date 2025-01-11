from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
  pass


class Candles(Base):
  __tablename__ = 'candles'
  id = Column(Integer(), primary_key=True)
  figi = Column(String(16), nullable=False)
  open = Column(Float(), nullable=False)
  high = Column(Float(), nullable=False)
  low = Column(Float(), nullable=False)
  close = Column(Float(), nullable=False)
  volume = Column(Integer(), nullable=False)
  time = Column(DateTime(), nullable=False)
  is_complete = Column(Boolean(), default=0, nullable=False)
  indicator = relationship('Indicators', backref='candle', uselist=False)
  param = relationship('Params', backref='candle', uselist=False)
  param_normal = relationship('Params_normal', backref='candle', uselist=False)
  prediction = relationship('Predictions', backref='candle', uselist=False)


class Indicators(Base):
  __tablename__ = 'indicators'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  weekday = Column(Integer(), nullable=False)
  session = Column(Integer(), nullable=False)
  session_len = Column(Integer(), nullable=False)  # константа
  s_min = Column(Integer(), nullable=False)

  open = Column(Float(), nullable=False)
  high = Column(Float(), nullable=False)
  low = Column(Float(), nullable=False)
  close = Column(Float(), nullable=False)
  ADX9 = Column(Float(), nullable=False)
  ADX9_pos = Column(Float(), nullable=False)
  ADX9_neg = Column(Float(), nullable=False)
  EMA24 = Column(Float(), nullable=False)
  EMA100 = Column(Float(), nullable=False)
  EMA200 = Column(Float(), nullable=False)
  MACD10_signal = Column(Float(), nullable=False)
  MACD12_24 = Column(Float(), nullable=False)
  RSI9 = Column(Float(), nullable=False)

  EMA24_volume = Column(Float(), nullable=False)
  EMA100_volume = Column(Float(), nullable=False)
  EMA200_volume = Column(Float(), nullable=False)
  max_volume = Column(Integer(), nullable=False, default=0)  # константа
  volume = Column(Float(), nullable=False)
  md_volume = Column(Float(), nullable=False)  # константа


class Params(Base):
  __tablename__ = 'params'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  wday_C = Column(Float(), nullable=False)
  s_min_C = Column(Float(), nullable=False)

  co_C = Column(Float(), nullable=False)
  hl_C = Column(Float(), nullable=False)
  hc_CP = Column(Float(), nullable=False)

  MACD10_P = Column(Float(), nullable=False)
  MACD10_C = Column(Float(), nullable=False)
  сEMA24_C = Column(Float(), nullable=False)
  сEMA24_P = Column(Float(), nullable=False)
  cEMA_100_C = Column(Float(), nullable=False)
  cEMA_100_P = Column(Float(), nullable=False)
  cEMA_200_C = Column(Float(), nullable=False)
  cEMA_200_P = Column(Float(), nullable=False)
  RSI9_C = Column(Float(), nullable=False)
  RSI9_P = Column(Float(), nullable=False)
  ADX9_C = Column(Float(), nullable=False)
  ADX9_P = Column(Float(), nullable=False)
  DI9_C = Column(Float(), nullable=False)
  DI9_P = Column(Float(), nullable=False)

  vEMA24_C = Column(Float(), nullable=False)
  vEMA24_P = Column(Float(), nullable=False)
  vEMA100_C = Column(Float(), nullable=False)
  vEMA100_P = Column(Float(), nullable=False)
  vEMA200_C = Column(Float(), nullable=False)
  vEMA200_P = Column(Float(), nullable=False)
  s_vol_C = Column(Float(), nullable=False)
  d_vol_CP = Column(Float(), nullable=False)


class Params_normal(Base):
  __tablename__ = 'params_normal'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  wday_C = Column(Float(), nullable=False)
  s_min_C = Column(Float(), nullable=False)

  co_C = Column(Float(), nullable=False)
  hl_C = Column(Float(), nullable=False)
  hc_CP = Column(Float(), nullable=False)

  MACD10_P = Column(Float(), nullable=False)
  MACD10_C = Column(Float(), nullable=False)
  сEMA24_C = Column(Float(), nullable=False)
  сEMA24_P = Column(Float(), nullable=False)
  cEMA_100_C = Column(Float(), nullable=False)
  cEMA_100_P = Column(Float(), nullable=False)
  cEMA_200_C = Column(Float(), nullable=False)
  cEMA_200_P = Column(Float(), nullable=False)
  RSI9_C = Column(Float(), nullable=False)
  RSI9_P = Column(Float(), nullable=False)
  ADX9_C = Column(Float(), nullable=False)
  ADX9_P = Column(Float(), nullable=False)
  DI9_C = Column(Float(), nullable=False)
  DI9_P = Column(Float(), nullable=False)

  vEMA24_C = Column(Float(), nullable=False)
  vEMA24_P = Column(Float(), nullable=False)
  vEMA100_C = Column(Float(), nullable=False)
  vEMA100_P = Column(Float(), nullable=False)
  vEMA200_C = Column(Float(), nullable=False)
  vEMA200_P = Column(Float(), nullable=False)
  s_vol_C = Column(Float(), nullable=False)
  d_vol_CP = Column(Float(), nullable=False)


class Predictions(Base):
  __tablename__ = 'predictions'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  high_10min = Column(Integer(), nullable=False)


# __table_args__ = (
#         ForeignKeyConstraint(['user_id'], ['users.id']),
#         Index('title_content_index' 'title', 'content'), # composite index on title and content
#     )
