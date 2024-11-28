from typing import Optional, List, Dict, Annotated
from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import User, Post
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse
from database import Base, engine, session_local

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    'http://127.0.0.1:8080/',
    'http://localhost:8080/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{name}", response_model=DbUser)
async def get_user(name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[DbUser])
async def get_user(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    if db_users is List[None]:
        raise HTTPException(status_code=404, detail="User not found")
    return db_users



@app.delete('/users/delete/{name}', response_model=DbUser)
async def delete_one_user(name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exists")
    db.delete(db_user)
    db.commit()
    return db_user

@app.delete('/users/delete/all', response_model=List[DbUser])
async def delete_all_users(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="Users not exist")
    for user in db_users:
        db.delete(user)
    db.commit()
    db.refresh(db_users)
    return db_users

@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_post = Post(title=post.title, body=post.body, author_id=db_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> List:
    db_posts = db.query(Post).all()
    return db_posts
