from pydantic import Field, BaseModel
from datetime import date

class StudentSchema(BaseModel):
    student_id : str =   Field()
    dob : date =   Field()
    first_name : str =   Field()
    last_name : str =  Field()
    email : str = Field()
    contact_no : str =   Field()
    gender : str =   Field()
    city : str =  Field()
    street : str =  Field()
    status : str =  Field()
    current_class : str =  Field()
    hashed_password : str = Field()
