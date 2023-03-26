import sys
import logging
import uvicorn
import time
from fastapi import FastAPI, Request
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

app.include_router(users.router, prefix="/users",)
app.include_router(tasks.router, prefix="/tasks",)
app.include_router(auth.router, prefix="/auth",)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger.info(f"requested at {start_time}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"resposne time {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
