from fastapi import APIRouter,HTTPException,Response,status,Depends
from routes.users_router.auth_logic import pass_settings
from sqlalchemy.future import select
from schemas.user_schemas.user_register import UserRegister
from schemas.user_schemas.user_auth import UserAuth
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
from db.session import get_db
from cruds.users_crud.crud import UserCRUD
from db.models.user import User
from services.jwt import create_access_token


router = APIRouter(prefix='/user_reg',tags=['Auth'])

@router.post('/register/')
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await UserCRUD.create_user(db, user_data)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }
    
@router.post('/login/')
async def auth_user(response:Response,user_data: UserAuth,db: AsyncSession = Depends(get_db)):
    password_str = user_data.password.get_secret_value()
    user = await User.check_user(name=user_data.name,password=password_str,db=db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect name or password")
    
    access_token = await create_access_token({"sub" : str(user['id'])})
    response.set_cookie(key='users_access_token',value=access_token,httponly=True)

    if response:
        return "Access successed"

    

