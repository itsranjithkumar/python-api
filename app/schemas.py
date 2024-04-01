from pydantic import BaseModel


class postBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class postCreate(postBase):
    pass



class post(BaseModel):
    id: int 
    title:str
    content: str
    published: bool

class config:
    orm_mode = True