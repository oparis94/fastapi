from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from .hashing import Hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Blog
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blogdb(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
# Delete Blog
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    db.query(models.Blogdb).filter(models.Blogdb.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Delete successfully"}

# Update Blog
@app.put("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blogdb).filter(models.Blogdb.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="is not available")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated"

# Get all
@app.get("/blog", response_model=List[schemas.ShowBlog])
def show_all_blog(db: Session = Depends(get_db)):
    all_blog = db.query(models.Blogdb).all()
    return all_blog

# Get blog with id
@app.get("/blog/{id}", response_model=schemas.ShowBlog)
def show_blog_with_id(id, response: Response, db: Session = Depends(get_db)):
    blog_with_id = db.query(models.Blogdb).filter(models.Blogdb.id == id).first()
    if not blog_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Not find blog with id {id}"}
    return blog_with_id

# Create User
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Userdb(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Show user with ID
@app.get("/user/{id}", response_model=schemas.ShowUser)
def show_user_with_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Userdb).filter(models.Userdb.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not available")
    return user