import uuid
from typing import Annotated, List, Dict
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from src.config.db import PSQLConfig
from src.v1 import models, controllers


# DB config and initialization
DB = PSQLConfig()

# Session for dependency injection
SessionDep = Annotated[Session, Depends(DB.get_session)]

# CORS allowances
origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    DB.create_db_and_tables()

@app.get("/")
async def helth_check():
    return {"status": "I'm functional and healthy!"}

@app.post("/api/v1/language")
def add_language(session: SessionDep, data: models.LanguageUpdate) -> models.Language:
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).add_item(data=data)

@app.get("/api/v1/languages")
def list_languages(session: SessionDep,
    offset: int=0,
    limit: Annotated[int, Query(le=100)] = 100
) -> List[models.Language]:
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).list_items(limit=limit, offfset=offset)

@app.get("/api/v1/language/{language_id}")
def get_language(session: SessionDep, language_id: uuid.UUID) -> models.Language:
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).get_item(id=language_id)

@app.delete("/api/v1/language/{language_id}")
def delete_language(session: SessionDep, language_id: uuid.UUID) -> Dict:
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).delete_item(id=language_id)

@app.patch("/api/v1/language/{language_id}")
def update_language(
    session: SessionDep,
    language_id: uuid.UUID,
    data: models.LanguageUpdate
) -> models.Language:
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).update_item(id=language_id, data=data)

@app.post("/api/v1/header")
def add_header(data: models.HeaderCreate, session: SessionDep) -> models.Header:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).add_item(data=data)

@app.get("/api/v1/headers")
def list_headers(session: SessionDep,
    offset: int=0,
    limit: Annotated[int, Query(le=100)] = 100
) -> List[models.Header]:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).list_items(limit=limit, offfset=offset)

@app.get("/api/v1/header/{header_id}")
def get_header(session: SessionDep, header_id: uuid.UUID) -> models.Header:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).get_item(id=header_id)

@app.get("/api/v1/language/{language_id}/header")
def get_header_by_language(session: SessionDep, language_id: uuid.UUID) -> models.Header:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).get_item_by_language(language_id=language_id)

@app.delete("/api/v1/header/{header_id}")
def delete_header(session: SessionDep, header_id: uuid.UUID) -> Dict:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).delete_item(id=header_id)

@app.patch("/api/v1/header/{header_id}")
def update_header(
    session: SessionDep,
    header_id: uuid.UUID,
    data: models.HeaderUpdate
) -> models.Header:
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).update_item(id=header_id, data=data)