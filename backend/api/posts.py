from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, User
from schemas import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
def get_feed(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    result = []
    for p in posts:
        result.append(PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            image_url=p.image_url,
            author_id=p.author_id,
            author_email=p.author.email,
            created_at=p.created_at,
        ))
    return result


@router.post("/", response_model=PostResponse)
def create_post(post_data: PostCreate, author_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")

    post = Post(
        title=post_data.title,
        content=post_data.content,
        image_url=post_data.image_url,
        author_id=author_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        author_id=post.author_id,
        author_email=user.email,
        created_at=post.created_at,
    )


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    db.delete(post)
    db.commit()
    return {"message": "Пост удалён по решению совета"}
