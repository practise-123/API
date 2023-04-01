import sys
sys.path.append("..")

from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import session
from schemas.students import StudentSchema
from routers.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_my_record(
    usr : StudentSchema = Depends(get_current_user)
    , db: session = Depends(get_db)
    ):
    return usr

@router.put("/")
async def update_my_record():
    pass