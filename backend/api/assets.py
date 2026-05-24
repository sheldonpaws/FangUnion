from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Asset, User
from schemas import AssetCreate, AssetResponse

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=list[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).order_by(Asset.created_at.desc()).all()
    result = []
    for a in assets:
        result.append(AssetResponse(
            id=a.id,
            title=a.title,
            description=a.description,
            image_url=a.image_url,
            asset_type=a.asset_type,
            owner_id=a.owner_id,
            owner_username=a.owner.username,
            created_at=a.created_at,
        ))
    return result


@router.post("/", response_model=AssetResponse)
def create_asset(asset_data: AssetCreate, owner_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Товарищ не найден")

    asset = Asset(
        title=asset_data.title,
        description=asset_data.description,
        image_url=asset_data.image_url,
        asset_type=asset_data.asset_type,
        owner_id=owner_id,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return AssetResponse(
        id=asset.id,
        title=asset.title,
        description=asset.description,
        image_url=asset.image_url,
        asset_type=asset.asset_type,
        owner_id=asset.owner_id,
        owner_username=user.username,
        created_at=asset.created_at,
    )
