from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class TeamRegister(BaseModel):
    name: str = Field(..., title="Название команды")
    photo_url: Optional[HttpUrl] = Field(None, title="Аватарка команды")
    organization: int = Field(..., title="Айди организации")
    region: str = Field(..., title="Регион")
    leader: str = Field(..., title="Руководитель")
    member_count: int = Field(..., title="Количество участников", ge=1)
    workspace_folder: Optional[str] = Field(None, title="Рабочая папка")

    completed_tasks: Optional[int] = Field(0, title="Количество выполненных дел", ge=0)
    team_star: Optional[float] = Field(0.0, title="Звезда команды", ge=0)
    pulse_solutions: Optional[int] = Field(0, title="Решений в Пульсе", ge=0)
    pulse_messages: Optional[int] = Field(0, title="Сообщений в Пульсе", ge=0)