from fastapi import Body, Depends, FastAPI,Response,status,HTTPException, APIRouter,Depends
from sqlalchemy.orm import Session
from.. import schemas, database, models, oauth2



router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votes: schemas.Vote,db: Session = Depends (database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post=db.query(models.post).filter(models.post.id == votes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {votes.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id, models.Votes.
         user_id == current_user.id)
    
    found_vote = vote_query.first()
    if (votes.dir == 1):       
        if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy voted on post {votes.post_id}")
        
        new_vote = models.Votes(post_id = votes.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist") 
        vote_query.delete(synchronize_session=False)
        db.commit()

        return