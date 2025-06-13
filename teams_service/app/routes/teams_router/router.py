from fastapi import APIRouter, Depends

from teams_service.app.shemas.team_shemas.team_register import TeamRegister
from teams_service.app.cruds.teams_crud.crud import TeamCRUD

from teams_service.app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/register")
async def register_team(team_data: TeamRegister, db: AsyncSession = Depends(get_db)):
    team = await TeamCRUD.create_team(db, team_data)
    return {
        "message": "Team registered successfully",
        "team_id": team.id
    }

