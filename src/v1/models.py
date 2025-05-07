import uuid
from datetime import datetime
from typing import Literal
from src.v1.enums import Language

from sqlalchemy import Uuid
from sqlmodel import Field, SQLModel, String, DateTime

class Language(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: Literal[Language.pt_br, Language.en_us] = Field(sa_type=String)
    description: str
    created_at: datetime = Field(index=True)
    updated_at: datetime | None = Field(index=True)

class LanguageCreate(SQLModel):
    name: str
    description: str

class LanguageUpdate(SQLModel):
    name: str | None
    description: str | None

class Header(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    image_url: str
    image_alt: str
    name: str
    title: str
    language_id: uuid.UUID = Field(foreign_key="language.id")

class HeaderCreate(SQLModel):
    image_url: str
    image_alt: str
    name: str
    title: str
    language_id: uuid.UUID = Field(foreign_key="language.id")

class HeaderUpdate(SQLModel):
    image_url: str | None
    image_alt: str | None
    name: str | None
    title: str | None
    language_id: uuid.UUID | None = Field(foreign_key="language.id")
