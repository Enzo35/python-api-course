from collections import UserDict
from pyexpat import model
from typing import Optional, List
from typing_extensions import deprecated
import bcrypt
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from httpx import delete
import psycopg2
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

# === API ====

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

