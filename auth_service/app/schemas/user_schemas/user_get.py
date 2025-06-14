from pydantic import BaseModel,Field


class UserGet(BaseModel):
    
    name: str = Field(..., example="userexample")