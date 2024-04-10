from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command

# SQLALCHEMY_DATABASE_URL = f'postgresql://itsranjithkumar:password@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
print(SQLALCHEMY_DATABASE_URL)
print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)






@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture()
def client (session):
    def overrid_get_db():

     try:
          yield session
     finally:
        session.close()
    app.dependency_overrides[get_db] = overrid_get_db

    yield TestClient(app)