from __future__ import annotations
from auth_service.app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False)

    