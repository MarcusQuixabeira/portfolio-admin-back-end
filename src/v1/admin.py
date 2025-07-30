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

@router.post("/languages", status_code=status.HTTP_200_OK)
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

@router.get("/languages/{language_id}", status_code=status.HTTP_200_OK)
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

@router.delete("/languages/{language_id}", status_code=status.HTTP_200_OK)
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

@router.patch("/languages/{language_id}", status_code=status.HTTP_200_OK)
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

@router.post("/headers", status_code=status.HTTP_200_OK)
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

@router.get("/headers/{header_id}", status_code=status.HTTP_200_OK)
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

@router.get("/languages/{language_id}/headers", status_code=status.HTTP_200_OK)
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

@router.delete("/headers/{header_id}")
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

@router.patch("/headers/{header_id}", status_code=status.HTTP_200_OK)
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

# ABOUT ME
@router.post("/about-mes", status_code=status.HTTP_200_OK)
def add_about_me( session: SessionDep, user_id: UserIdDep, data: models.AboutMeCreate) -> models.AboutMe:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).add_item(data=data)

@router.get("/about-mes", status_code=status.HTTP_200_OK)
def list_about_mes(session: SessionDep,
    user_id: UserIdDep,
    offset: int=0,
    limit: Annotated[int, Query(le=100)] = 100
) -> List[models.AboutMe]:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).list_items(limit=limit, offfset=offset)

@router.get("/about-mes/{about_me_id}", status_code=status.HTTP_200_OK)
def get_about_me(session: SessionDep, user_id: UserIdDep, about_me_id: uuid.UUID) -> models.AboutMe:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).get_item(id=about_me_id)

@router.get("/languages/{language_id}/about-mes", status_code=status.HTTP_200_OK)
def get_about_me_by_language(session: SessionDep, user_id: UserIdDep, language_id: uuid.UUID) -> models.AboutMe:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).get_item_by_language(language_id=language_id, status_code=status.HTTP_200_OK)

@router.delete("/about-mes/{about_me_id}")
def delete_about_me(session: SessionDep, user_id: UserIdDep, about_me_id: uuid.UUID) -> Dict:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).delete_item(id=about_me_id)

@router.patch("/about-mes/{about_me_id}", status_code=status.HTTP_200_OK)
def update_about_me(
    session: SessionDep, user_id: UserIdDep,
    about_me_id: uuid.UUID,
    data: models.AboutMeUpdate
) -> models.AboutMe:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    return controllers.BaseController(
        session=session,
        model_class=models.AboutMe,
        create_class=models.AboutMeCreate,
        update_class=models.AboutMeUpdate,
        language=None
    ).update_item(id=about_me_id, data=data)