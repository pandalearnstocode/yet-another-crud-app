import os
import logging
from typing import List
import uuid
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from models import ModelDB, ModelSchema, Model
from db import SessionLocal
from db import engine
from models import Base
from curd import crud_post, crud_get, crud_get_all, crud_put, crud_delete
from worker.celery_app import celery_app

log = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()


def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))


@app.get("/{word}")
async def root(word: str, background_task: BackgroundTasks):
    task_name = None

    # set correct task name based on the way you run the example
    if not bool(os.getenv('DOCKER')):
        task_name = "app.worker.celery_worker.test_celery"
    else:
        task_name = "app.app.worker.celery_worker.test_celery"

    task = celery_app.send_task(task_name, args=[word])
    print(task)
    background_task.add_task(background_on_message, task)

    return {"message": "Word received"}

@app.post("/model/", response_model=ModelDB, status_code=201)
def create_model(*, db: Session = Depends(get_db), payload: ModelSchema):
    model = crud_post(db_session=db, payload=payload)
    return model

@app.get("/model/{id}/", response_model=ModelDB)
def read_model(
    *,
    db: Session = Depends(get_db),
    id: uuid.UUID,
):
    model = crud_get(db_session=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@app.get("/model/", response_model=List[ModelDB])
def read_all_models(db: Session = Depends(get_db)):
    return crud_get_all(db_session=db)

@app.put("/model/{id}/", response_model=ModelDB)
def update_model(*, db: Session = Depends(get_db), id: uuid.UUID, payload: ModelSchema):
    model = crud_get(db_session=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud_put(
        db_session=db,
        model=model,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        country=payload.country,
        email=payload.email,
        user_group=payload.user_group,
    )
    return model


@app.delete("/model/{id}/", response_model=ModelDB)
def delete_model(
    *,
    db: Session = Depends(get_db),
    id: uuid.UUID,
):
    model = crud_get(db_session=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud_delete(db_session=db, id=id)
    return model


###############################################################################
# from typing import List
# import os
# import logging

# from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
# from sqlalchemy.orm import Session
# import uuid
# from app.api import crud
# from app.api.models import ModelDB, ModelSchema
# from app.db import SessionLocal

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# @router.post("/", response_model=ModelDB, status_code=201)
# def create_model(*, db: Session = Depends(get_db), payload: ModelSchema):
#     model = crud.post(db_session=db, payload=payload)
#     return model


# @router.get("/{id}/", response_model=ModelDB)
# def read_model(
#     *,
#     db: Session = Depends(get_db),
#     id: uuid.UUID,
# ):
#     model = crud.get(db_session=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     return model


# @router.get("/", response_model=List[ModelDB])
# def read_all_models(db: Session = Depends(get_db)):
#     return crud.get_all(db_session=db)


# @router.put("/{id}/", response_model=ModelDB)
# def update_model(*, db: Session = Depends(get_db), id: uuid.UUID, payload: ModelSchema):
#     model = crud.get(db_session=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     model = crud.put(
#         db_session=db,
#         model=model,
#         title=payload.title,
#         description=payload.description,
#         status=payload.status,
#         country=payload.country,
#         email=payload.email,
#         user_group=payload.user_group,
#     )
#     return model


# @router.delete("/{id}/", response_model=ModelDB)
# def delete_model(
#     *,
#     db: Session = Depends(get_db),
#     id: uuid.UUID,
# ):
#     model = crud.get(db_session=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     model = crud.delete(db_session=db, id=id)
#     return model


# @router.get("/{word}")
# async def root(word: str, background_task: BackgroundTasks):
#     task_name = None
#     task_name = "app.worker.celery_worker.test_celery"
#     task = celery_app.send_task(task_name, args=[word])
#     print(task)
#     background_task.add_task(background_on_message, task)
#     return {"message": "Word received"}