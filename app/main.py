from argparse import OPTIONAL
from collections import UserDict
import dbm
from operator import index
from typing import Optional
from urllib import response
from webbrowser import get
from click import password_option
from fastapi import Body, Depends, FastAPI,Response,status,HTTPException
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel

from random import randrange
from psycopg2.extras import RealDictCursor
import time
from  sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db 
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)


app = FastAPI()



# class post(BaseModel):
#     title: str
#     content: str 
#     published: bool = True  
    
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

   

   
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"favorite food", "content":"I like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i    
        

        
        
app.include_router(post.router)  
app.include_router(user.router)  
app.include_router(auth.router) 

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):

#     posts = db.query(models.post).all()
     
#     print(posts)
#     return {"data": "successfull"}

# @app.get("/posts", response_model= list [schemas.post])
# def get_posts(db: Session = Depends (get_db)):
#     #cursor.execute("""SELECT * FROM posts """)
#     #posts = cursor.fetchall() 
#     posts = db.query(models.post).all()
#     return posts

# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.post)
# def create_posts(post: schemas.postCreate, db: Session = Depends(get_db)):
    
#     #NEW_POST = cursor.execute("""INSERT INTO POSTS (title, content, published) values(%s,%s,%s) RETURNING* """,(post.title, post.content,post.published))
#     #NEW_POST = cursor.fetchone()

#     #conn.commit()
    
#     new_post = models.post( 
#         **post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return  new_post
  

# @app.get("/posts/{id}", response_model=schemas.post)
# def get_post(id:int, db: Session = Depends(get_db)):
#    # cursor.execute("""SELECT *from posts WHERE id = %s""",(str(id)))
#    # post = cursor.fetchone()
#     post = db.query(models.post).filter(models.post.id ==id).first()
    

#     if not post:
        
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
       
#     return  post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
    
#     #cursor.execute("""DELETE FROM THE posts WHERE id = %s returning *""", (str(id),))
#     #deleted_post = cursor.fetchone
#     #conn.commit()
#     post = db.query(models.post).filter(models.post.id ==id)

#     if post.first() == None:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
#     post.delete(synchronize_session=False)
#     db.commit()

#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model = schemas.post)
# def update_post(id: int, updated_post: schemas.postCreate, db: Session = Depends(get_db)):
#     #cursor.execute("""UPDATE posts SET title = %s,content =%s, published = %s RETURNING *""",(post.title,post.content,post.published))
#     #updated_post = cursor.fetchone()
#     #conn.commit()

#     post_query = db.query(models.post).filter(models.post.id == id)
   
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

#     post_query.update(updated_post.model_dump(), synchronize_session=False)

#     db.commit()
#     return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def Create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.user(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model = schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db),):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user 