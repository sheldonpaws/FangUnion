# ☭ FangUnion — Союз Клыков

> Социальная сеть для фурри-сообщества в ретро-коммунистическом стиле.

## О проекте

FangUnion — это социальная сеть, где каждый фурри может найти свою стаю. Посты, асеты, профили и многое другое — всё в духе советской ретро-эстетики.

**Автор:** Шелдон Павс

## Стек

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, JavaScript

## Запуск

```bash
cd backend
uvicorn main:app --reload
```

Сервер запустится на `http://localhost:8000`

Документация API: `http://localhost:8000/docs`

## Структура

```
FangUnion/
├── backend/
│   ├── main.py          # Точка входа
│   ├── database.py      # Подключение к SQLite
│   ├── models.py        # Модели (User, Post, Asset)
│   ├── schemas.py       # Pydantic схемы
│   └── api/
│       ├── users.py     # Регистрация, авторизация, профили
│       ├── posts.py     # Лента постов
│       └── assets.py    # Асеты (арт, бейджи, рамки)
├── frontend/
│   ├── index.html       # Главная (лента)
│   ├── login.html       # Вход / Регистрация
│   ├── profile.html     # Профиль
│   ├── assets.html      # Асеты
│   ├── style.css        # Ретро-стиль
│   └── app.js           # Логика
└── requirements.txt
```

## Лицензия

MIT
