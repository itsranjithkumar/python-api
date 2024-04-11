from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
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


@pytest.fixture
def test_user(client):
      user_data = {"email":"aaa4956@gmail.com",
    "password":"hjhgf"}
      res = client.post("/users/", json=user_data)

      assert res.status_code == 201
      print(res.json())
      new_user = res.json()
      new_user['password'] = user_data['password']
      return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
     client.headers = {
         **client.headers,
         "Authorization": f"Bearer {token}"
     }

     return client