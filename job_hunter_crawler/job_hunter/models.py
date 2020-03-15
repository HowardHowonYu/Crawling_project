from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine("mysql://root:dss@15.164.136.109/job_hunter",encoding='utf-8')


def create_channel_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Channels(DeclarativeBase):
    """Sqlalchemy deals model"""
    
    __tablename__ = "job_hunter"

    id = Column(Integer, primary_key=True)
    
    ## 테이블 설정
    company_name = Column('company_name', String(1000), nullable=True)
    business = Column('business', String(3000), nullable=True)
    position = Column('position', String(3000), nullable=True)
    link = Column('link', String(5000), nullable=True)
    salary_condition = Column('salary_condition', String(50), nullable=True)
    deadline = Column('deadline', String(500), nullable=True)
    keyword = Column('keyword', String(3000), nullable=True)
    location = Column('location', String(500), nullable=True)


    