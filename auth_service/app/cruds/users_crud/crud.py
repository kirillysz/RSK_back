from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from routes.users_router.auth_logic import pass_settings

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
        
    async def get_all_users(db: AsyncSession):
        try:
            result = await db.execute(select(User))
            users = result.scalars().all()
            
            if not users:  
                return []
                
            return users
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while fetching users: {str(e)}"
            )

    async def delete_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        try:
            await db.delete(user)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error while deleting user: {str(e)}"
            )