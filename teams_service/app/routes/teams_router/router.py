from fastapi import APIRouter, Depends, HTTPException

from app.shemas.team_shemas.team_register import TeamRegister
from app.cruds.teams_crud.crud import TeamCRUD

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/register")
async def register_team(team_data: TeamRegister, db: AsyncSession = Depends(get_db)):
    team = await TeamCRUD.create_team(db, team_data)
    return {
        "message": "Team registered successfully",
        "team_id": team.id
    }

@router.get('/all_teams/')
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    teams = await TeamCRUD.get_all_teams(db)
    return teams

@router.delete('/delete_team/{team_id}')
async def delete_team(
    team_id: int,  
    db: AsyncSession = Depends(get_db)
):
    try:
        await TeamCRUD.delete_team(db, team_id)
        return {"message": f"Team {team_id} deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )
