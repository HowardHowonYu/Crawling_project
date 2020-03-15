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
    return create_engine("mysql://root:dss@15.164.136.109/job_hunter")


def create_channel_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Channels(DeclarativeBase):
    """Sqlalchemy deals model"""
    
    __tablename__ = "job_hunter"

    id = Column(Integer, primary_key=True)
    
    ## 테이블 설정
    date = Column('date', DateTime)
    company_name = Column(String(1000))
    business = Column(String(3000))
    position = Column(String(3000))
    link = Column(String(5000))
    salary_condition = Column(String(50))
    deadline = Column( String(5000))
    keyword = Column(String(3000))
    location = Column(String(500))

    def __init__(self, id=None, date=None, company_name=None, business=None, position=None, link=None, salary_condition=None, deadline=None, keyword=None, location=None):
        self.id = id
        self.date = date
        self.company_name = company_name
        self.business = business
        self.position = position
        self.link = link
        self.salary_condition = salary_condition
        self.deadline = deadline
        self.keyword = keyword
        self.location = location
    