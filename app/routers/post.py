from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import models, schemas, utils, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/alchemy",
    tags=['Posts']
)

# === API WITH SQLALCHEMY ===

@router.get("/get")
def al_get_posts(db: Session = Depends(get_db), limit: int = 10, skip: Optional[int] = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return {"data": posts}

@router.get("/get/{id}")
def al_get_one_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data": post}

@router.post("/post", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def al_post_posts(payload: schemas.Post, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    #post = models.Post(title=payload.title, content=payload.content, published=payload.published, owner_id=curr_user.id)
    #post = models.Post(**payload.dict(), owner_id=curr_user.id)
    post = models.Post(**payload.dict(), owner_id=curr_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/del/{id}")
def al_delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    if post.owner_id != int(curr_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform rquested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/put/{id}")
def al_put_post(id: int, payload: schemas.Post, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    if post.owner_id != int(curr_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform rquested action")
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
