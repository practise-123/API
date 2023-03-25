from sqlalchemy import Column, Integer, Boolean, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Users(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    last_updated_dt = Column(Date, onupdate=func.now())


class Tasks(Base):
    __tablename__ = "tasks"
    tid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    created_dt = Column(Date, nullable=False, server_default=func.now())
    last_updated_dt = Column(Date, nullable=False, onupdate=func.now())
    uid = Column(Integer, ForeignKey(Users.uid))
