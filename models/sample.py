from sqlalchemy import Column, Integer, String

from settings import Base


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String)

    def __repr__(self):
        return "<Sample('data={}')>".format(self.data)
