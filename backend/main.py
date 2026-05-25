import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.users import router as users_router
from api.posts import router as posts_router
from api.assets import router as assets_router

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

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


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(400, "Только изображения: JPEG, PNG, GIF, WebP")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    import uuid
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(400, "Файл слишком большой (макс. 5 МБ)")
        f.write(content)

    return {"url": f"/uploads/{filename}"}


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
