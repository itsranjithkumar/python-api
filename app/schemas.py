import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime

from typing import Annotated




class postBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class postCreate(postBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class config:
    orm_mode = True
 
class post(postBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class config:
        orm_mode = True


class postOut(postBase):
    id: int 
    created_at: datetime
    owner_id: int
    owner: UserOut

class config:
    orm_mode = True



class User(BaseModel):
    post: post
    votes: int

    class config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    Token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]