from pydantic import BaseModel, Field, validator
from datetime import date, datetime

class TaskInSchema(BaseModel):
    title: str
    description: str = Field(default=None)
    status: str = Field(default=None)
    
class TaskOutSchema(TaskInSchema):
    tid: int
    uid: int
    created_dt: date = Field(default=None)
    last_updated_dt: date = Field(default=None)
    
    class Config:
        orm_mode = True

    # @validator("created_dt")
    # def parse_created_date(cls, v):
    #     if v:
    #         return v
        
    # @validator("updated_dt")
    # def parse_updated_date(cls, v):
    #     if v:
    #         return v
    


class UserInSchema(BaseModel):
    username: str
    full_name: str = Field(default= None)
    email: str = Field(default= None)
    password: str

class UserOutSchema(BaseModel):
    uid: int
    username: str
    full_name: str
    email: str
    is_active: bool
    hashed_password: str
    last_updated_dt: date

class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str  = Field(default=None)