from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root@localhost:3306/QualityControl_db'

engine = create_engine(URL_DATABASE)


Base = declarative_base()
