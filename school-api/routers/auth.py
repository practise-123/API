import sys 
sys.path.append("..")
import logging
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from settingsConfig import SettingsSchema
from sqlalchemy.orm import session
from database import get_db
from models import StudentsModel
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)

settings = SettingsSchema()

PWD_CONTEXT = CryptContext(schemes= settings.CRYPT, deprecated= 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
        headers={"WWW-Authenticate": "Bearer"},
    )
router = APIRouter()

def get_user(usrNm, typ, db):
    if typ == "STUDENT":
        usr = db.query(StudentsModel).filter(StudentsModel.student_id == usrNm).first()
    if usr :
        return usr
    else:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_bearer)
                     , db: session = Depends(get_db)):
    try:
        logger.info("Validating user")
        paylod = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITH)
        usrnm = paylod.get('sub')
        usrTyp = paylod.get("type")
        if not usrnm and not usrTyp:
            raise credentials_exception
        else:
            usr = get_user(usrnm, usrTyp, db)
        if usr is None:
                raise credentials_exception
        logger.info(f"Token Validated")
        return usr
    except JWTError:
        raise credentials_exception


def verify_password(pwd, hshdPwd):
    return PWD_CONTEXT.verify(secret=pwd, hash=hshdPwd)

def authenticate_user(db, usrnm, pwd):
    user = db.query(StudentsModel).filter(StudentsModel.student_id == usrnm).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found")
    if not verify_password(pwd, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or pwd")
    else: 
        return user

def create_access_token(data, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITH)
    return encoded_jwt


@router.post("/token")
async def get_access_token(
        formdata : OAuth2PasswordRequestForm = Depends()
        , db : session = Depends(get_db)
    ):
    logger.info(f"Authenticating user : {formdata.username}")
    user = authenticate_user(db, formdata.username, formdata.password)
    if not user:
        raise credentials_exception
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.student_id, "type":"STUDENT"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}