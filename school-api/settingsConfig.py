from pydantic import BaseSettings

class SettingsSchema(BaseSettings):
    SECRET_KEY : str = 'QWERTYasdfghjklmnbvcxflaornql'
    ALGORITH : str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 40
    CRYPT : list = ['bcrypt']
    
