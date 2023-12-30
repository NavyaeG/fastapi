from pydantic import BaseModel,EmailStr,StrictStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Config:

    orm_mode=True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class User(BaseModel,Config):
    id: int
    email: EmailStr
    created_at: datetime

class PostO(PostBase,Config):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

class PostOut(BaseModel,Config):
    Post: PostO
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel,Config):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[StrictStr]=None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)