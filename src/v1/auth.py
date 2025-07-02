import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from passlib.context import CryptContext
from src.v1.models import User, Token
from src.config.db import PSQLConfig
from jose import jwt, JWTError


SECRET_KEY = os.environ['JWT_SECRET_KEY']
ALGORITHM = os.environ['JWT_ALGORITHM']

# DB config and initialization
DB = PSQLConfig()

# Session for dependency injection
SessionDep = Annotated[Session, Depends(DB.get_session)]

router = APIRouter(
  prefix='/api/v1',
  tags=['Auth'],
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/token')


@router.post('/token', response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='username and/or password are invalid.')
    token = create_access_token(user.username, str(user.id), timedelta(minutes=10))
    return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, session: Session) -> User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: str, expiration_delta: timedelta):
    exp = datetime.now(timezone.utc) + expiration_delta
    payload = {
        'sub': 'user',
        'id': user_id,
        'exp': int(exp.timestamp())
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('id')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the token.')
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate the token or token is expired.')