import random
import string
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
from models import User, Reward
from schemas import UserCreate, UserResponse, UserLogin


def generate_passport_number(db: Session, length: int = 8) -> str:
    """Генерирует уникальный номер паспорта формата FK-XXXXXXXX (буквы A-Z + цифры 0-9)."""
    chars = string.ascii_uppercase + string.digits
    for _ in range(1000):
        suffix = ''.join(random.choices(chars, k=length))
        number = f"FK-{suffix}"
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
        plain_password=user_data.password,
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
    # Начисляем награду за регистрацию
    welcome_reward = Reward(user_id=user.id, amount=100, reason="Регистрация в Союзе Клыков")
    db.add(welcome_reward)
    db.commit()
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


@router.get("/recover", response_model=UserResponse)
def recover_password(passport_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.passport_number == passport_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="Аккаунт с таким номером паспорта не найден")
    return user


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


@router.patch("/{user_id}/status")
def update_status(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    if "is_online" in data:
        user.is_online = data["is_online"]
    if "last_visit" in data:
        lv = data["last_visit"]
        if isinstance(lv, str):
            lv = datetime.fromisoformat(lv.replace("Z", "+00:00"))
        user.last_visit = lv
    if "post_count" in data:
        user.post_count = data["post_count"]
    if "story_count" in data:
        user.story_count = data["story_count"]
    if "image_count" in data:
        user.image_count = data["image_count"]
    if "music_count" in data:
        user.music_count = data["music_count"]
    if "daily_login_streak" in data:
        user.daily_login_streak = data["daily_login_streak"]
    if "daily_login_last" in data:
        user.daily_login_last = data["daily_login_last"]
    if "help_count" in data:
        user.help_count = data["help_count"]
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


def get_rank_by_balance(balance: int) -> str:
    if balance >= 100000:
        return "Легенда"
    elif balance >= 50000:
        return "Мастер"
    elif balance >= 20000:
        return "Герой"
    elif balance >= 10000:
        return "Ветеран"
    elif balance >= 5000:
        return "Активист"
    elif balance >= 2000:
        return "Гражданин"
    elif balance >= 500:
        return "Участник"
    return "Новичок"


# Награды за действия
CREATIVE_REWARDS = {
    "post": 10,           # Пост/объявление
    "story": 50,          # Рассказ
    "image": 30,          # Изображение/арт
    "music": 40,          # Музыка/песня
    "avatar": 20,         # Загрузка аватара
    "profile_complete": 50,  # Заполнение профиля
    "daily_login": 5,     # Ежедневный вход
    "help_others": 15,    # Помощь другим
}

@router.post("/{user_id}/reward")
def add_reward(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    amount = data.get("amount", 0)
    reason = data.get("reason", "")
    user.balance = (user.balance or 0) + amount
    user.rank = get_rank_by_balance(user.balance)
    reward = Reward(user_id=user_id, amount=amount, reason=reason)
    db.add(reward)
    db.commit()
    db.refresh(user)
    return {"ok": True, "balance": user.balance, "rank": user.rank}


@router.post("/{user_id}/reward/action")
def reward_action(user_id: int, data: dict, db: Session = Depends(get_db)):
    """Начисляет награду за действие: post, story, image, music, avatar, daily_login, profile_complete"""
    action = data.get("action", "")
    amount = CREATIVE_REWARDS.get(action, 0)
    if not amount:
        raise HTTPException(status_code=400, detail=f"Неизвестное действие: {action}")
    reasons = {
        "post": "Публикация поста",
        "story": "Публикация рассказа",
        "image": "Загрузка изображения",
        "music": "Публикация музыки",
        "avatar": "Загрузка аватара",
        "profile_complete": "Заполнение профиля",
        "daily_login": "Ежедневный вход",
        "help_others": "Помощь другим",
    }
    return add_reward(user_id, {"amount": amount, "reason": reasons.get(action, action)}, db)


@router.post("/{user_id}/daily-login")
def daily_login(user_id: int, db: Session = Depends(get_db)):
    """Ежедневный вход с прогрессивной наградой: 5, 15, 25, 35... за каждый день подряд. Сброс при пропуске."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")
    now = datetime.utcnow()
    last = user.daily_login_last
    streak = user.daily_login_streak or 0
    if last:
        diff_days = (now - last).days
        if diff_days == 0:
            return {"ok": True, "message": "Сегодня уже получено", "streak": streak, "balance": user.balance}
        elif diff_days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
    amount = 5 + (streak - 1) * 10
    user.daily_login_streak = streak
    user.daily_login_last = now
    user.balance = (user.balance or 0) + amount
    user.rank = get_rank_by_balance(user.balance)
    reward = Reward(user_id=user_id, amount=amount, reason=f"Ежедневный вход (день {streak})")
    db.add(reward)
    db.commit()
    db.refresh(user)
    return {"ok": True, "amount": amount, "streak": streak, "balance": user.balance, "rank": user.rank}


@router.get("/{user_id}/rewards")
def get_rewards(user_id: int, db: Session = Depends(get_db)):
    rewards = db.query(Reward).filter(Reward.user_id == user_id).order_by(Reward.created_at.desc()).limit(20).all()
    return [{"id": r.id, "amount": r.amount, "reason": r.reason, "created_at": r.created_at} for r in rewards]
