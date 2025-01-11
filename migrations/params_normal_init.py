from sqlalchemy import create_engine
import internal.domain.models as models

engine = create_engine('sqlite:///storage/sqlite/shares.db')
engine.connect()

models.Base.metadata.create_all(engine, tables=[models.Params_normal.__table__])
