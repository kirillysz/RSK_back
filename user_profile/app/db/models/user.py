from __future__ import annotations
from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from db.models.user_enum import UserEnum

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    NameIRL: Mapped[str] = mapped_column(String(100))  # Added reasonable length
    Surname: Mapped[str] = mapped_column(String(100))
    Patronymic: Mapped[str] = mapped_column(String(100))
    Description: Mapped[str] = mapped_column(String(500))
    Region: Mapped[str] = mapped_column(String(100))
    Type: Mapped[UserEnum] = mapped_column(SQLEnum(UserEnum), nullable=False)
    Organization: Mapped[str] = mapped_column(String(100))
    team: Mapped[str] = mapped_column(String(100))

    

    