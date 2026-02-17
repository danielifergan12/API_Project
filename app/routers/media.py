from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.media_item import MediaItem, MediaType
from app.schemas.media import Media, MediaCreate, MediaUpdate

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/", response_model=Media, status_code=status.HTTP_201_CREATED)
async def create_media_item(
    media_in: MediaCreate,
    db: AsyncSession = Depends(get_db),
) -> Media:
    media = MediaItem(**media_in.model_dump())
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


@router.get("/", response_model=List[Media])
async def list_media_items(
    title: Optional[str] = Query(default=None),
    type: Optional[MediaType] = Query(default=None),
    year: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[Media]:
    stmt: Select = select(MediaItem)

    conditions = []
    if title:
        conditions.append(MediaItem.title.ilike(f"%{title}%"))
    if type:
        conditions.append(MediaItem.type == type)
    if year:
        conditions.append(MediaItem.year == year)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{media_id}", response_model=Media)
async def get_media_item(
    media_id: int,
    db: AsyncSession = Depends(get_db),
) -> Media:
    result = await db.execute(select(MediaItem).where(MediaItem.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")
    return media


@router.put("/{media_id}", response_model=Media)
async def update_media_item(
    media_id: int,
    media_in: MediaUpdate,
    db: AsyncSession = Depends(get_db),
) -> Media:
    result = await db.execute(select(MediaItem).where(MediaItem.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

    for field, value in media_in.model_dump(exclude_unset=True).items():
        setattr(media, field, value)

    await db.commit()
    await db.refresh(media)
    return media


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media_item(
    media_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(select(MediaItem).where(MediaItem.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

    await db.delete(media)
    await db.commit()
    return None


