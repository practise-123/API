import uvicorn
from fastapi import FastAPI
from routers import tasks

app = FastAPI(
    title="Tasks",
    description="List of tasks",
    version="0.1.0"
)
app.include_router(tasks.router, prefix="/tasks",)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
