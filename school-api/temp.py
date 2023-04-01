import sys
import json
import logging
from models import StudentsModel
from database import SessionLocale
from fastapi import Depends
from passlib.context import CryptContext
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API Started")
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
CLASSES = ['First','Second','Third','Forth','Fifth','Sixth','Seventh','Eighth','Nineth','Tenth']

def load_student_data(db = SessionLocale()):
    now = date.today()
    with open(f"./data/students.json", 'r') as fl:
        jsonData = json.load(fl)
        for rec in jsonData:
            rec['hashed_password'] = PWD_CONTEXT.hash(rec.get('student_id'))
            dob = datetime.strptime(rec.get('dob'), '%Y-%m-%d' )
            diffyears = relativedelta(now, dob).years
            if diffyears<3:
                rec['current_class'] = 'KG'
            elif diffyears<=5:
                rec['current_class'] = 'First'
            elif diffyears<15 and diffyears>=6:
                c = diffyears-5
                rec['current_class'] = CLASSES[c]
            elif diffyears>=15:
                rec['current_class']  = 'Tenth'
            dtrec = StudentsModel(**rec)
            db.add(dtrec)
            db.commit()


if __name__ == "__main__":
    globals()[sys.argv[1]]()

