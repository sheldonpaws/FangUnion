from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- User ---

class UserCreate(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = None
    species: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    display_name: Optional[str]
    species: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
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
    author_username: str
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
    owner_username: str
    created_at: datetime

    class Config:
        from_attributes = True
