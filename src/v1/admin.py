import uuid
import time
from typing import Annotated, List, Dict
from src.config.db import PSQLConfig
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from src.v1 import models, controllers
from starlette import status
from src.v1.auth import verify_token

# DB config and initialization
DB = PSQLConfig()

# Session for dependency injection
SessionDep = Annotated[Session, Depends(DB.get_session)]
UserIdDep = Annotated[str, Depends(verify_token)]


router = APIRouter(
  prefix='/api/v1',
  tags=['Admin'],
)

@router.get('/get_current_user', response_model=models.CurrentUser, status_code=status.HTTP_200_OK)
def get_user(session: SessionDep, user_id: UserIdDep) -> models.CurrentUser:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the user.')
    return user

@router.get('/verify_token', status_code=status.HTTP_200_OK)
def verify_token(user_id: UserIdDep):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return {'token is valid'}

@router.post("/language", status_code=status.HTTP_200_OK)
def add_language(session: SessionDep, user_id: UserIdDep, data: models.LanguageUpdate) -> models.Language:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).add_item(data=data)

@router.get("/languages", status_code=status.HTTP_200_OK)
def list_languages(session: SessionDep,
    user_id: UserIdDep,
    offset: int=0,
    limit: Annotated[int, Query(le=100)] = 100
) -> List[models.Language]:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).list_items(limit=limit, offfset=offset)

@router.get("/language/{language_id}", status_code=status.HTTP_200_OK)
def get_language(session: SessionDep, user_id: UserIdDep, language_id: uuid.UUID) -> models.Language:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).get_item(id=language_id)

@router.delete("/language/{language_id}", status_code=status.HTTP_200_OK)
def delete_language(session: SessionDep, user_id: UserIdDep, language_id: uuid.UUID) -> Dict:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).delete_item(id=language_id)

@router.patch("/language/{language_id}", status_code=status.HTTP_200_OK)
def update_language(
    session: SessionDep,
    user_id: UserIdDep,
    language_id: uuid.UUID,
    data: models.LanguageUpdate
) -> models.Language:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Language,
        create_class=models.LanguageCreate,
        update_class=models.LanguageUpdate,
        language=None
    ).update_item(id=language_id, data=data)

@router.post("/header", status_code=status.HTTP_200_OK)
def add_header( session: SessionDep, user_id: UserIdDep, data: models.HeaderCreate) -> models.Header:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).add_item(data=data)

@router.get("/headers", status_code=status.HTTP_200_OK)
def list_headers(session: SessionDep,
    user_id: UserIdDep,
    offset: int=0,
    limit: Annotated[int, Query(le=100)] = 100
) -> List[models.Header]:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).list_items(limit=limit, offfset=offset)

@router.get("/header/{header_id}", status_code=status.HTTP_200_OK)
def get_header(session: SessionDep, user_id: UserIdDep, header_id: uuid.UUID) -> models.Header:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).get_item(id=header_id)

@router.get("/language/{language_id}/header", status_code=status.HTTP_200_OK)
def get_header_by_language(session: SessionDep, user_id: UserIdDep, language_id: uuid.UUID) -> models.Header:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).get_item_by_language(language_id=language_id, status_code=status.HTTP_200_OK)

@router.delete("/header/{header_id}")
def delete_header(session: SessionDep, user_id: UserIdDep, header_id: uuid.UUID) -> Dict:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).delete_item(id=header_id)

@router.patch("/header/{header_id}", status_code=status.HTTP_200_OK)
def update_header(
    session: SessionDep, user_id: UserIdDep,
    header_id: uuid.UUID,
    data: models.HeaderUpdate
) -> models.Header:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.Header,
        create_class=models.HeaderCreate,
        update_class=models.HeaderUpdate,
        language=None
    ).update_item(id=header_id, data=data)