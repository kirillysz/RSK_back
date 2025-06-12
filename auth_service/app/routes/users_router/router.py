from fastapi import APIRouter,HTTPException,Response,status,Depends

from auth_service.app.routes.users_router.auth_logic import pass_settings
from auth_service.app.schemas.user_schemas.user_register import UserRegister

from auth_service.app.db.models.user import User
from auth_service.app.db.session import get_db
from auth_service.app.cruds.users_crud.crud import UserCRUD

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/user_reg',tags=['Auth'])

@router.post('/register/')
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await UserCRUD.create_user(db, user_data)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }
    
    

    

