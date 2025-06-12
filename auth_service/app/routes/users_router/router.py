from fastapi import APIRouter,HTTPException,Response,status,Depends
from routes.users_router.auth_logic import pass_settings
from sqlalchemy.future import select
from schemas.user_schemas.user_register import UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
from db.session import get_db
from cruds.users_crud.crud import UserCRUD

router = APIRouter(prefix='/user_reg',tags=['Auth'])

@router.post('/register/')
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await UserCRUD.create_user(db, user_data)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }
    
    

    

