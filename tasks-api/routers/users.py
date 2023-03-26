import sys
sys.path.append("..")

import logging
from datetime import date
from fastapi import APIRouter, Query, Form, HTTPException, status, Depends
from sqlalchemy.orm import session

from routers.auth import get_hashed_password, get_current_user, verify_password
from models import Users
from schemas import UserInSchema, UserOutSchema
from database import get_db

logger = logging.getLogger("tasks-api.log")
router = APIRouter(
    tags= ['Users']
)

@router.post("/")
async def register_user(
    username: str = Form(),
    full_name : str = Form(default=None),
    email : str = Form(default=None),
    password : str = Form(),
    confirm_password : str = Form(),
    db: session = Depends(get_db)
):
    logger.debug(f"{username}")
    if (not username) and (not password) and (not confirm_password):
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE)
    if not (password == confirm_password):
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE)
    hsd_pwd = get_hashed_password(password)
    user = Users(
        username = username,
        full_name = full_name,
        email = email,
        is_active = True,
        hashed_password = hsd_pwd
    )
    db.add(user)
    db.commit()
    return user

@router.put("/")
async def update_user_details(
        full_name : str = Form(default=None)
        , email : str = Form(default= None)
        , password : str = Form(default=None)
        , confirm_password: str = Form(default=None)
        , db: session = Depends(get_db)
        , usr : UserOutSchema = Depends(get_current_user)
    ):
    if not usr:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    user = db.query(Users).filter(Users.uid == usr.uid).first()
    if full_name:
        user.full_name = full_name
    if email :
        user.email = email
    if password and len(password)>0 :
        if password == confirm_password:
            pwd = get_hashed_password(password)
            user.hashed_password = pwd
    user.last_updated_dt = date.today()
    db.add(user)
    db.flush()
    db.commit()
    logger.info(f"Update succesfull")

@router.delete("/")
async def delete_my_account(
        password : str = Form()
        , usr: UserOutSchema = Depends(get_current_user)
        , db: session = Depends(get_db)
    ):
    logger.info(f"Deleting the account")
    if not usr:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)
    is_pwd_correct = verify_password(password, usr.hashed_password)  
    if is_pwd_correct:
        user = db.query(Users).filter(Users.uid == usr.uid).first()
        db.delete(user)
    else:
        logger.info(f"Inccorect password")
    db.flush()
    db.commit()
    logger.info(f"Delete succesfull")