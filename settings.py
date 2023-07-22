from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = 'sqlite:///db.sqlite3'

# Engine の作成
Engine = create_engine(
    path,
    echo=False
)
Base = declarative_base()
Session = sessionmaker(bind=Engine)
