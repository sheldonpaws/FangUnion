import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserLogin


def generate_passport_number(db: Session) -> str:
    """Генерирует уникальный номер паспорта формата FK-XXXXXX."""
    for _ in range(100):
        number = f"FK-{random.randint(100000, 999999)}"
        if not db.query(User).filter(User.passport_number == number).first():
            return number
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать уникальный номер паспорта")


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
        birth_year=user_data.birth_year,
        birth_place=user_data.birth_place,
        form=user_data.form,
        profession=user_data.profession,
        avatar_url=user_data.avatar_url,
        passport_number=generate_passport_number(db),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == credentials.email,
        User.passport_number == credentials.passport_number,
    ).first()
    if not user or not check_password_hash(user.password_hash, credentials.password):
        raise HTTPException(status_code=401, detail="Неверный email, номер паспорта или пароль!")
    return {"message": "Добро пожаловать в Союз Клыков!", "user_id": user.id}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    return user


@router.patch("/{user_id}/avatar")
def update_avatar(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    user.avatar_url = data.get("avatar_url")
    db.commit()
    db.refresh(user)
    return {"ok": True}


@router.patch("/{user_id}/bio")
def update_bio(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    user.bio = data.get("bio", "")
    db.commit()
    db.refresh(user)
    return {"ok": True}


@router.patch("/{user_id}")
def update_profile(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    fields = ["display_name", "species", "birth_year", "birth_place", "form", "profession", "backstory", "biography", "aforism"]
    for f in fields:
        if f in data:
            setattr(user, f, data[f])
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/password")
def change_password(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    old = data.get("old_password", "")
    new = data.get("new_password", "")
    if not check_password_hash(user.password_hash, old):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="Пароль слишком короткий")
    user.password_hash = generate_password_hash(new)
    db.commit()
    return {"ok": True}
