from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, oauth2, schemas

from .. import database, schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login( user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):

    
    user = db.query(models.user).filter(models.user.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")
    
    #create a token
    #return token

    access_token = oauth2.create_access_token(data ={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}