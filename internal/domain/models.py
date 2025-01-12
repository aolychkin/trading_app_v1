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
  session = Column(Integer(), nullable=False)

  high = Column(Float(), nullable=False)
  low = Column(Float(), nullable=False)
  close = Column(Float(), nullable=False)
  ADX9 = Column(Float(), nullable=False)
  ADX9_pos = Column(Float(), nullable=False)
  ADX9_neg = Column(Float(), nullable=False)
  EMA24 = Column(Float(), nullable=False)
  MACD10_signal = Column(Float(), nullable=False)
  MACD12_24 = Column(Float(), nullable=False)
  RSI9 = Column(Float(), nullable=False)

  EMA24_volume = Column(Float(), nullable=False)
  volume = Column(Float(), nullable=False)


class Params(Base):
  __tablename__ = 'params'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  hl_C = Column(Float(), nullable=False)

  MACD10 = Column(Float(), nullable=False)  # Из гугл таблицы: пересечение и сила
  сEMA24 = Column(Float(), nullable=False)  # Просто Close выше или ниже EMA24
  RSI9 = Column(Float(), nullable=False)  # Сигналом является только: Выход из "зоны" комфорта
  ADX9 = Column(Float(), nullable=False)  # Растущий и высокий тренд (больше 25 и чем больше - тем лучше) = подтверждение продажи и покупки. "Для ADX все что не рост - все слабость тренда"
  DI9 = Column(Float(), nullable=False)

  vEMA24 = Column(Float(), nullable=False)
  # middle_vol = Column(Float(), nullable=False)


class Params_normal(Base):
  __tablename__ = 'params_normal'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  hl_C = Column(Float(), nullable=False)

  MACD10 = Column(Float(), nullable=False)  # Из гугл таблицы: пересечение и сила
  сEMA24 = Column(Float(), nullable=False)  # Просто Close выше или ниже EMA24
  RSI9 = Column(Float(), nullable=False)  # Сигналом является только: Выход из "зоны" комфорта
  ADX9 = Column(Float(), nullable=False)  # Растущий и высокий тренд (больше 25 и чем больше - тем лучше) = подтверждение продажи и покупки. "Для ADX все что не рост - все слабость тренда"
  DI9 = Column(Float(), nullable=False)

  vEMA24 = Column(Float(), nullable=False)


class Predictions(Base):
  __tablename__ = 'predictions'
  id = Column(Integer(), primary_key=True)
  candle_id = Column(Integer(), ForeignKey('candles.id'))

  high_10min = Column(Integer(), nullable=False)


# __table_args__ = (
#         ForeignKeyConstraint(['user_id'], ['users.id']),
#         Index('title_content_index' 'title', 'content'), # composite index on title and content
#     )
