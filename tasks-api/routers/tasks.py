import sys
sys.path.append("..")

import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body
from models import Tasks
from schemas import TaskInSchema, TaskOutSchema
from database import SessionLocale, get_db
router = APIRouter(
    tags=['Tasks']
)
logger = logging.getLogger(__name__)

@router.get("/",
            # response_model= list[TaskOutSchema]
            )
async def get_all_tasks(db: Annotated[SessionLocale, Depends(get_db)]):
    task_list = db.query(Tasks).all()
    return task_list

@router.post("/")
async def add_task(
    db: Annotated[SessionLocale, Depends(get_db)],
    title: Annotated[str, Query()],
    description: Annotated[str, Query()],
    status: Annotated[str, Query()],
):
    task = TaskInSchema(
        title= title,
        description= description,
        status= status
    )

    tm = Tasks(
        uid=1,
        title = task.title,
        description = task.description,
        status = task.description,
        created_dt="03-23-2023", 
        last_updated_dt="03-23-2023",
        )
    db.add(tm)
    db.commit()
    return task