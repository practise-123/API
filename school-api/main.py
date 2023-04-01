import logging
import uvicorn
from fastapi import FastAPI
from routers import students, auth
logging.basicConfig(filename="school-api.log", filemode='w+', level=logging.DEBUG
                    , format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API Started")

app = FastAPI(
    title= " My School API"
    , description= "This is a school api"
    , version= "0.0.1"
)
app.include_router(students.router, prefix="/students", tags=['Students'])
app.include_router(auth.router, prefix='/auth', tags=['Authorization'])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)