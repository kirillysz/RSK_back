from __future__ import annotations
from auth_service.app.db.base import Base
from auth_service.app.db.models.teams_enums.enums import DirectionEnum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    direction = Column(Enum(DirectionEnum), nullable=False)
    photo_url = Column(String)
    city = Column(String)
    region = Column(String)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="teams")

    leader_id = Column(Integer, ForeignKey("users.id"))
    leader = relationship("User", back_populates="leading_teams")

