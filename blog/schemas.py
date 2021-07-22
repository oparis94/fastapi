from pydantic import BaseModel

 # A pydantic model
class Blog(BaseModel):
    id: int
    title: str
    body: str
