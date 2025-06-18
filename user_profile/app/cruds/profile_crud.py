from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from fastapi import HTTPException


class ProfileCRUD:
    @staticmethod
    async def create_profile(db: AsyncSession, profile_data):
        exiting_profile = await db.execute(
            select(User).where(User.NameIRL == profile_data.NameIRL)
        )
        if exiting_profile.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Team already exists"
            )

        new_profile = User(
            NameIRL=profile_data.NameIRL,
            Surname = profile_data.Surname,
            Patronymic = profile_data.Patronymic,
            Description = profile_data.Description,
            Region = profile_data.Region,
            Type = profile_data.Type,
            Organization = profile_data.Organization,
            Organization_id = profile_data.Organization_id,
            team_id = profile_data.team_id,
            team = profile_data.team
            
        )

        db.add(new_profile)

        try:
            await db.commit()
            await db.refresh(new_profile)
            return new_profile

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while registering team: {str(e)}"
            )
    
    
    