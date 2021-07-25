from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, SessionLocal, get_db
from .hashing import Hash
from .routers import blog

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog.router)

# Create User
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Userdb(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Show user with ID
@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["Users"])
def show_user_with_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Userdb).filter(models.Userdb.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not available")
    return user