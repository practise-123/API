import logging
import uvicorn
from fastapi import FastAPI
from routers import tasks, users
import models
from database import engine

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# logger = logging.getLogger(__name__)
# fileHandler = logging.FileHandler("task-api.log")
# fileHandler.setFormatter(logFormatter)
# logger.addHandler(fileHandler)
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# logger.addHandler(consoleHandler)


models.Base.metadata.create_all(bind= engine)

app = FastAPI(
    title="Tasks",
    description="List of tasks",
    version="0.1.0"
)
app.include_router(users.router, prefix="/users",)
app.include_router(tasks.router, prefix="/tasks",)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
