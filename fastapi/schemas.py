from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic V2 replacement for `orm_mode`
    }

class PostBase(BaseModel):
    title: str
    body: str
    author_id: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: User

    model_config = {
        "from_attributes": True  # Pydantic V2 replacement for `orm_mode`
    }