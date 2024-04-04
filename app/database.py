from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time




SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:

    try:
        conn = psycopg2.connect(host='localhost', database= 'fastapi', user = 'postgres',password='password', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("database connection was succesfull!")
        break
    except Exception as error:
        print("connection to database failed")
        print ("error:", error)
        time.sleep(2)