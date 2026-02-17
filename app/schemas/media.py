from typing import Optional

from pydantic import BaseModel, Field

from app.models.media_item import MediaType


class MediaBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    type: MediaType
    year: Optional[int] = Field(default=None, ge=1800, le=2100)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class MediaCreate(MediaBase):
    pass


class MediaUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    type: Optional[MediaType] = None
    year: Optional[int] = Field(default=None, ge=1800, le=2100)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class MediaInDBBase(MediaBase):
    id: int

    class Config:
        from_attributes = True


class Media(MediaInDBBase):
    pass


