from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONNECTION_URL = 'postgresql://postgres:Postgres143!@localhost/learning'
schema_name = 'school-api'
engine = create_engine(url=CONNECTION_URL)
SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData(schema=schema_name)
Base = declarative_base(metadata= meta)

def get_db():
    try:
        db = SessionLocale()
        yield db
    finally:
        db.close()