from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.teams import Team
from fastapi import HTTPException


class TeamCRUD:
    @staticmethod
    async def create_team(db: AsyncSession, team_data):
        exiting_team = await db.execute(
            select(Team).where(Team.name == team_data.name)
        )
        if exiting_team.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Team already exists"
            )

        new_team = Team(
            name=team_data.name,
            direction=team_data.direction,
            city=team_data.city,
            region=team_data.region,
            organization_id=team_data.organization_id,
            leader_id=team_data.leader_id,
            
        )

        db.add(new_team)

        try:
            await db.commit()
            await db.refresh(new_team)
            return new_team

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while registering team: {str(e)}"
            )
    
    @staticmethod
    async def delete_team(db: AsyncSession, team_id):
        exiting_team = await db.execute(
            select(Team).where(Team.id == team_id)
        )
        team = exiting_team.scalar_one_or_none()
        
        if team is not None:
            raise HTTPException(
                status_code=404,
                detail=f"Team with id {team_id} not found"
            )
        
        await db.delete(team)

        try:
            await db.commit()
            return {"detail": f"Team with id {team_id} deleted successfully"}
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while deleting team: {str(e)}"
            )
        
    