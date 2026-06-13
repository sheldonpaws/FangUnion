from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    plain_password = Column(String(255), nullable=False)
    display_name = Column(String(100))
    species = Column(String(50))
    birth_year = Column(String(20))
    birth_place = Column(String(100))
    form = Column(String(50))
    profession = Column(String(100))
    avatar_url = Column(String(500))
    backstory = Column(Text, default="")
    biography = Column(Text, default="")
    aforism = Column(String(500), default="")
    passport_number = Column(String(20), unique=True, index=True)
    last_visit = Column(DateTime, default=datetime.utcnow)
    is_online = Column(Integer, default=0)
    post_count = Column(Integer, default=0)
    balance = Column(Integer, default=100)
    rank = Column(String(50), default="Новичок")
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author")
    assets = relationship("Asset", back_populates="owner")
    rewards = relationship("Reward", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    image_url = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    image_url = Column(String(255), nullable=False)
    asset_type = Column(String(50))  # art, badge, avatar_frame, etc.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="assets")


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rewards")
