from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.app.db.models.teams import Team
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
            photo_url=team_data.photo_url,
            city=team_data.city,
            region=team_data.region,
            organization_id=team_data.organization_id,
            leader_id=team_data.leader_id,
            folder_url=team_data.folder_url,
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