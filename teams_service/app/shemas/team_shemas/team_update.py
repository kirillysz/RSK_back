from pydantic import BaseModel, Field
from app.db.models.teams_enums.enums import DirectionEnum

class TeamUpdate(BaseModel):
    name: str = Field(..., title="Название команды")
    direction: DirectionEnum = Field(..., title="Направление команды")
    city: str = Field(..., title="Город")
    region: str = Field(..., title="Регион")
    organization_id: int = Field(..., title="ID организации")
    leader_id: int = Field(..., title="ID лидера")