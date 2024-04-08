import json
from fastapi import Body, Depends, FastAPI,Response,status,HTTPException, APIRouter,Depends
from  sqlalchemy.orm import Session
from typing import List
from typing import Optional
from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db
from operator import index
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags= ['users']
)

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.post).all()
     
    print(posts)
    return {"data": "successfull"}

# @router.get("/", response_model= list [schemas.post])
@router.get("/", response_model= List[schemas.postOut])
def get_posts(db: Session = Depends (get_db), current_user : int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional [str] = ""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall() 
   
    print(search)
    print("aaaaaaaaaaaaaaaaaa")
    posts = db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()
    print("bbbbbbbbbbbbbbbbbbbb")

    results = db.query(models.post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.post.id, isouter=True).group_by(models.post.id).first()
    print("cccccccccccccccccc")
   
   

   
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.post)
def create_posts(post: schemas.postCreate, db: Session = Depends(get_db), current_user :  int = Depends(oauth2.get_current_user)):
    
    #NEW_POST = cursor.execute("""INSERT INTO POSTS (title, content, published) values(%s,%s,%s) RETURNING* """,(post.title, post.content,post.published))
    #NEW_POST = cursor.fetchone()

    #conn.commit()
     
    new_post = models.post(owner_id=current_user.id,
        **post.model_dump())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post
  

@router.get("/{id}", response_model=schemas.post)
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT *from posts WHERE id = %s""",(str(id)))
   # post = cursor.fetchone()
    post = db.query(models.post).filter(models.post.id ==id).first()
    

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
       
    
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #cursor.execute("""DELETE FROM THE posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone
    #conn.commit()
    post_query = db.query(models.post).filter(models.post.id ==id)
     
    post = post_query.first()

    if post.first() == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.post)
def update_post(id: int, updated_post: schemas.postCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s,content =%s, published = %s RETURNING *""",(post.title,post.content,post.published))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.post).filter(models.post.id == id)
   
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
        
    db.commit()
    return post_query.first()