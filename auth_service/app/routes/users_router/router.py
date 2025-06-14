
from fastapi import APIRouter,HTTPException,Response,status,Depends
from schemas.user_schemas.user_register import UserRegister
from schemas.user_schemas.user_auth import UserAuth
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
from db.session import get_db
from cruds.users_crud.crud import UserCRUD
from db.models.user import User
from services.jwt import create_access_token

from fastapi import APIRouter,Depends

from schemas.user_schemas.user_register import UserRegister

from db.session import get_db
from cruds.users_crud.crud import UserCRUD

from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter(prefix='/users_interaction',tags=['AuthSystem'])

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
    
@router.get('/get_users/')
async def get_all_users(db: AsyncSession = Depends(get_db)):
    
    try:
        users = await UserCRUD.get_all_users(db)
        return users
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch users: {str(e)}"
        )
    
@router.delete('/delete_user/')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await UserCRUD.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
    

    

    

