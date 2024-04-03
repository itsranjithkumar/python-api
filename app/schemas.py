import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class postBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class postCreate(postBase):
    pass



class post(postBase):
    id: int 
    created_at: datetime

class config:
    orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class config:
    orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    Token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None