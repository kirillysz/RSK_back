from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.app.db.models.user import User
from auth_service.app.routes.users_router.auth_logic import pass_settings

from fastapi import HTTPException

class UserCRUD:
    @staticmethod
    async def create_user(db: AsyncSession, user_data):
        
        existing_user = await db.execute(
            select(User).where(User.name == user_data.name)
        )
        
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail='User already registered'
            )

        
        password_str = user_data.password.get_secret_value()
        hashed_password = pass_settings.get_password_hash(password_str)

        
        new_user = User(
            name=user_data.name,
            hashed_password=hashed_password,
            
        )
        
        db.add(new_user)
        
        try:
            await db.commit()
            await db.refresh(new_user)
            return new_user
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while registering user: {str(e)}"
            )