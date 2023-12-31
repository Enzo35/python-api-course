from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(
    prefix="/alchemy/users",
    tags=['Users']
)

# === API WITH SQLALCHEMY ===

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def al_create_user(payload: schemas.UserCreate , db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(payload.password)
    payload.password = hashed_pwd
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def al_get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return user