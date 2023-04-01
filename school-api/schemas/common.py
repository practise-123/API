from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    user_id : str = Field()
    user_name : str = Field()
    email : str = Field()
    first_name : str = Field()
    last_name : str = Field()