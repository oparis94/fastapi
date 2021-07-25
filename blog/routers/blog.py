from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter()

get_db = database.get_db

# Create Blog
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blogdb(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Show all Blog
@router.get("/blog", response_model=List[schemas.ShowBlog], tags=["Blogs"])
def show_all_blog(db: Session = Depends(get_db)):
    all_blog = db.query(models.Blogdb).all()
    return all_blog

# Delete Blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog(id, db: Session = Depends(get_db)):
    db.query(models.Blogdb).filter(models.Blogdb.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Delete successfully"}

# Update Blog
@router.put("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blogdb).filter(models.Blogdb.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="is not available")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated"

# Show Blog with ID
@router.get("/blog/{id}", response_model=schemas.ShowBlog, tags=["Blogs"])
def show_blog_with_id(id, response: Response, db: Session = Depends(get_db)):
    blog_with_id = db.query(models.Blogdb).filter(models.Blogdb.id == id).first()
    if not blog_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Not find blog with id {id}"}
    return blog_with_id