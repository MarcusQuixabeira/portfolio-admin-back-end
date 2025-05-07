import uuid
from datetime import datetime
from typing import Annotated, Optional
from fastapi import Body, Query
from sqlmodel import Session, select, SQLModel
from pydantic import BaseModel
from src.v1 import models

class DAOException(Exception):
    pass

class BaseDAO(object):
    def __init__(
        self,
        session: Session,
        model_class: SQLModel,
        create_class: SQLModel,
        update_class: SQLModel,
        language: Optional[str]=None
    ):
        self.model_class = model_class
        self.create_class = create_class
        self.update_class = update_class
        self.language = language
        self.session = session

    def add_item(self, data):
        item_data = data.model_dump()
        item_data['created_at'] = datetime.now()
        item = self.model_class(**item_data)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def list_items(
        self,
        offset: int=0,
        limit: Annotated[int, Query(le=100)] = 100
    ):
        items = self.session.exec(select(self.model_class).offset(offset).limit(limit)).all()
        return items

    def get_item(self, id: uuid.UUID):
        item = self.session.get(self.model_class, id)
        return item
    
    def get_item_by_language(self, language_id: uuid.UUID):
        pass

    def delete_item(self, id: uuid.UUID):
        item = self.get_item(id=id)
        if not item:
            raise DAOException(f"{self.model_class.__name__} with id {id} not found")
        self.session.delete(item)
        self.session.commit()

    def update_item(
        self,
        id: uuid.UUID,
        data
    ):
        db_item = self.get_item(id=id)
        if not db_item:
            raise DAOException(f"{self.model_class.__name__} with id {id} not found")
        item_data = data.model_dump(exclude_unset=True)
        item_data['updated_at'] = datetime.now()
        db_item.sqlmodel_update(item_data)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item
