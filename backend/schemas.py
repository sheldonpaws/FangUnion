from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- User ---

class UserCreate(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None
    species: Optional[str] = None
    birth_year: Optional[str] = None
    birth_place: Optional[str] = None
    form: Optional[str] = None
    profession: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str]
    species: Optional[str]
    birth_year: Optional[str] = None
    birth_place: Optional[str] = None
    form: Optional[str] = None
    profession: Optional[str] = None
    avatar_url: Optional[str] = None
    backstory: Optional[str] = ""
    biography: Optional[str] = ""
    aforism: Optional[str] = ""
    passport_number: Optional[str] = None
    plain_password: Optional[str] = None
    last_visit: Optional[datetime] = None
    is_online: Optional[int] = 0
    post_count: Optional[int] = 0
    balance: Optional[int] = 100
    rank: Optional[str] = "Новичок"
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    passport_number: str
    password: str


# --- Post ---

class PostCreate(BaseModel):
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    title: Optional[str]
    content: str
    image_url: Optional[str]
    author_id: int
    author_email: str
    author_avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Asset ---

class AssetCreate(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    asset_type: Optional[str] = "art"


class AssetResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: str
    asset_type: Optional[str]
    owner_id: int
    owner_email: str
    created_at: datetime

    class Config:
        from_attributes = True
