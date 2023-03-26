import sys
sys.path.append("..")
import logging
from fastapi import Response,Request, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Annotated
from database import get_db
from models import Users
from schemas import TokenSchema, TokenDataSchema

logger = logging.getLogger("./tasks-api.log")
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("Auth file")


SECRET_KEY = 'QWERTYasdfghjklmnbvcxflaornql'
ALGORITH = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 40
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    tags = ['Authentication']
)

def get_user(usrnm, db:session= Depends(get_db)):
    usr = db.query(Users).filter(Users.username == usrnm).first()
    if usr.is_active:
        return usr
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]
                     , db: session = Depends(get_db)
                ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info("Validating token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITH)
        usrnm = payload.get('sub')
        if usrnm is None:
            raise credentials_exception
        token_data = TokenDataSchema(username= usrnm)
        usr =  get_user(usrnm= token_data.username, db=db)
        if usr is None:
            raise credentials_exception
        logger.info(f"Token Validated")
        return usr
    except JWTError:
        raise credentials_exception
        
def authenticate_user(db, usrnm, pwd):
    user = db.query(Users).filter(Users.username==usrnm).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    else:
        is_valid = PWD_CONTEXT.verify(pwd, user.hashed_password)
    if is_valid:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

def create_access_token(data, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt

@router.post("/token")
async def get_token(response: Response
                    , formdata : OAuth2PasswordRequestForm= Depends()
                    , db: session = Depends(get_db)
                ):
    logger.info(f"Starting Authentication of {formdata.username}")
    user = authenticate_user(db, formdata.username, formdata.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User {formdata.username} has been authenticated")
    return {"access_token": access_token, "token_type": "bearer"}