import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.users import router as users_router
from api.posts import router as posts_router
from api.assets import router as assets_router

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FangUnion — Союз Клыков",
    description="Социальная сеть для фурри-сообщества. Все клыки вместе!",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(users_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(assets_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Да здравствует Союз Клыков! 🐾",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
