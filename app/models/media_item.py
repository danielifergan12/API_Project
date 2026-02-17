from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from . import Base


class MediaType(str, PyEnum):
    MOVIE = "movie"
    SERIES = "series"
    BOOK = "book"
    GAME = "game"


class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    type = Column(Enum(MediaType), nullable=False, index=True)
    year = Column(Integer, nullable=True, index=True)
    genre = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships will be completed once User and Review models exist
    # created_by = relationship("User", back_populates="media_items")
    # reviews = relationship("Review", back_populates="media_item", cascade="all, delete-orphan")


