from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserLogin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Этот email уже зарегистрирован!")

    user = User(
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        display_name=user_data.display_name,
        species=user_data.species,
        furry_since=user_data.furry_since,
        profession=user_data.profession,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not check_password_hash(user.password_hash, credentials.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль!")
    return {"message": "Добро пожаловать в Союз Клыков!", "user_id": user.id}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    return user
