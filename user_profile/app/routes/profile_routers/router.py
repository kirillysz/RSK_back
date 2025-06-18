
from fastapi import APIRouter,HTTPException,Response,status,Depends

from schemas.user import ProfileCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
from db.session import get_db
from cruds.profile_crud import ProfileCRUD
from db.models.user import User


from fastapi import APIRouter,Depends



from db.session import get_db

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/profile_interaction',tags=['ProfileSystem'])

@router.post('/create_profile/')
async def create_profile(profile_data: ProfileCreateSchema, db: AsyncSession = Depends(get_db)):
    user = await ProfileCRUD.create_profile(db, profile_data)
    return {
        "message": "successfully",
        
    }