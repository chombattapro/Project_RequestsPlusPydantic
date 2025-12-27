from pydantic import BaseModel

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str
