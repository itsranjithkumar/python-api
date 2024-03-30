
from argparse import OPTIONAL

from collections import UserDict

from operator import index
from typing import Optional
from click import password_option
from fastapi import Body, FastAPI,Response,status,HTTPException
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
    title: str
    content: str 
    published: bool = True
    
while True:

    try:
        conn = psycopg2.connect(host='localhost', database= 'postgres', user = 'postgres',password='password', cursor_factory=RealDictCursor )
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

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:post):
    
    cursor.execute("""INSERT INTO POSTS (title, content, published) values(%s,%s,%s)""",(post.title, post.content,post.published))
    return {"data":"created post"}


@app.get("/posts/{id}")
def get_post(id:int):
    
    post = find_post(id)
    if not post:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
       
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    #find the index in the array that has required id
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index]= post_dict
    return {'data': post_dict}