import sys
sys.path.append("..")

import logging
import json
from typing import Annotated
import fastapi
from fastapi import APIRouter, Request, Depends, Query, Body, HTTPException
from sqlalchemy.orm import session
from datetime import date

from models import Tasks
from schemas import TaskInSchema, TaskOutSchema, UserOutSchema
from database import  get_db
from routers.auth import get_current_user

router = APIRouter(
    tags=['Tasks']
)

logger = logging.getLogger("tasks-api.log")
# logger.addHandler(logging.StreamHandler(sys.stdout))

@router.get("/",
            response_model= list[TaskOutSchema]
            )
async def get_all_tasks(request: Request
        , db: session = Depends(get_db)
        , usr : UserOutSchema = Depends(get_current_user)
    ):
    logger.info(f"retreiving tasks for {usr.username}")
    task_list = db.query(Tasks).filter(Tasks.uid == usr.uid).all()
    return task_list

@router.post("/")
async def add_task(
    request: Request,
    title: str = Query(),
    description:str = Query(),
    status: str = Query(),
    db: session = Depends(get_db),
    usr : UserOutSchema = Depends(get_current_user)
):
    logger.info("Adding new task")
    task = TaskInSchema(
        title= title,
        description= description,
        status= status
    )

    tm = Tasks(
        uid= usr.uid,
        title = task.title,
        description = task.description,
        status = task.description,
        created_dt=  date.today(),
        last_updated_dt= date.today(),
        )
    db.add(tm)
    db.commit()
    logger.info(f"New Task added")
    return task

@router.put("/")
async def update_task(
    tid= Query(),
    new_title= Query(default= None),
    new_description = Query(default=None),
    new_status = Query(default=None),
    db: session = Depends(get_db),
    usr : UserOutSchema = Depends(get_current_user),
):
    logger.info(f"Updating task {tid}")
    existing_task = db.query(Tasks).filter(Tasks.uid == usr.uid).filter(Tasks.tid == tid).first()
    if not existing_task:
        raise HTTPException(status_code= fastapi.status.HTTP_404_NOT_FOUND)
    if new_title:
        existing_task.title = new_title
    if new_description:
        existing_task.description = new_description
    if new_status:
        existing_task.status = new_status
    existing_task.last_updated_dt = date.today()
    db.flush()
    db.commit()
    logger.info(f"task  updated")
    return existing_task.title

@router.delete("/")
async def delete_task(
        task_id = Query(),
        user: UserOutSchema = Depends(get_current_user),
        db: session = Depends(get_db)
    ):
    task = db.query(Tasks).filter(Tasks.tid == task_id and Tasks.uid == user.uid).first()
    db.delete(task)
    db.flush()
    db.commit()