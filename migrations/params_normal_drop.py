from sqlalchemy import create_engine
import internal.domain.models as models

engine = create_engine('sqlite:///storage/sqlite/shares.db')
engine.connect()

models.Params_normal.__table__.drop(engine)
