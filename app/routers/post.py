from fastapi import Body, Depends, FastAPI,Response,status,HTTPException, APIRouter
from  sqlalchemy.orm import Session
from typing import List

from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db
from operator import index


router = APIRouter(
    prefix= "/posts",
    tags= ['users']
)

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.post).all()
     
    print(posts)
    return {"data": "successfull"}

@router.get("/", response_model= list [schemas.post])
def get_posts(db: Session = Depends (get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall() 
    posts = db.query(models.post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.post)
def create_posts(post: schemas.postCreate, db: Session = Depends(get_db), user_id:  int = Depends(oauth2.get_current_user)):
    
    #NEW_POST = cursor.execute("""INSERT INTO POSTS (title, content, published) values(%s,%s,%s) RETURNING* """,(post.title, post.content,post.published))
    #NEW_POST = cursor.fetchone()

    #conn.commit()
    print(user_id)
    new_post = models.post( 
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post
  

@router.get("/{id}", response_model=schemas.post)
def get_post(id:int, db: Session = Depends(get_db)):
   # cursor.execute("""SELECT *from posts WHERE id = %s""",(str(id)))
   # post = cursor.fetchone()
    post = db.query(models.post).filter(models.post.id ==id).first()
    

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
       
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM THE posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone
    #conn.commit()
    post = db.query(models.post).filter(models.post.id ==id)

    if post.first() == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.post)
def update_post(id: int, updated_post: schemas.postCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s,content =%s, published = %s RETURNING *""",(post.title,post.content,post.published))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.post).filter(models.post.id == id)
   
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()