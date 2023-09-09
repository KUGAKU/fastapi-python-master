import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = os.environ.get("DATABASE_CONNECTION_STRING", "sqlite:///db.sqlite3")

# Engine の作成
Engine = create_engine(path, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=Engine)
