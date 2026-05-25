from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- User ---

class UserCreate(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None
    species: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str]
    species: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
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
