import sys
import logging
import uvicorn
from fastapi import FastAPI
from routers import tasks, users, auth
import models
from database import engine

logging.basicConfig(filename="tasks-api.log", filemode='w+', level=logging.DEBUG
                    , format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API Started")

models.Base.metadata.create_all(bind= engine)
app = FastAPI(
    title="Tasks",
    description="List of tasks",
    version="0.1.0"
)
# app.include_router(users.router, prefix="/users",)
app.include_router(tasks.router, prefix="/tasks",)
app.include_router(auth.router, prefix="/auth",)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
