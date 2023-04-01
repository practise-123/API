from sqlalchemy import Column, Integer, Boolean, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class StudentsModel(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True)
    dob= Column(Date, nullable=False)
    first_name= Column(String, nullable=False)
    last_name= Column(String)
    email= Column(String)
    contact_no= Column(String, nullable=False)
    gender= Column(String, nullable=False)
    city= Column(String)
    street= Column(String)
    status= Column(String)
    current_class= Column(String)
    hashed_password= Column(String)
