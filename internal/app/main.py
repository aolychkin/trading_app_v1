from sqlalchemy import create_engine
import internal.domain.models as models

if __name__ == '__main__':
  engine = create_engine('sqlite:///storage/sqlite/shares.db')
  engine.connect()
  models.Base.metadata.create_all(engine)
