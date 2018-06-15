from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
DB_connect = 'postgresql+psycopg2://oryssuczcsrgtv:08a41edbb9d5552eb061f84c07e64acf1e2a8cdbac20c9853219d5d7508ebc43@ec2-54-235-193-34.compute-1.amazonaws.com/d5hq8c33gg3161'


class Images(Base):
    __tablename__ = 'Images'

    id = Column(Integer, primary_key=True)
    Url = Column(String)
    CreateDate = Column(DateTime(timezone=True), server_default=func.now())

if __name__ == '__main__':
    engine = create_engine(DB_connect)
    session = sessionmaker()
    session.configure(bind=engine)
    print('Succeed!!!')
    Base.metadata.create_all(engine)
