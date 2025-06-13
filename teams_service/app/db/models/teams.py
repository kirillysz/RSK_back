from __future__ import annotations
from app.db.base import Base
from app.db.models.teams_enums.enums import DirectionEnum
from sqlalchemy import Column, Integer, String, Enum

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    direction = Column(Enum(DirectionEnum), nullable=False)
    photo_url = Column(String)
    city = Column(String)
    region = Column(String)
    organization_id = Column(Integer)
    leader_id = Column(Integer)