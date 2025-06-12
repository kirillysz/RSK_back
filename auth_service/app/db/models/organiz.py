from __future__ import annotations
from auth_service.app.db.base import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    region = Column(String)
    star_rating = Column(Integer, default=3)

    teams = relationship("Team", back_populates="organization")

