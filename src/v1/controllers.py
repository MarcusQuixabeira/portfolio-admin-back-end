import uuid
from typing import Optional
from sqlmodel import Session, SQLModel
from fastapi import HTTPException
from src.v1 import models
from src.v1.dao import BaseDAO, DAOException


class BaseController(object):
    def __init__(
        self,
        session: Session,
        model_class: SQLModel,
        create_class: SQLModel,
        update_class: SQLModel,
        language: Optional[str]=None,
    ):
        self.dao = BaseDAO(
            session = session,
            model_class = model_class,
            create_class = create_class,
            update_class = update_class,
            language = language
        )
        self.model_class = model_class
        self.create_class = create_class
        self.update_class = update_class
    
    def add_item(self, data):
        return self.dao.add_item(data=data)
    
    def list_items(self, offfset: int=0, limit: int=100):
        return self.dao.list_items(offset=offfset, limit=limit)

    def get_item(self, id: uuid.UUID):
        item = self.dao.get_item(id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
        return item
    
    def get_item_by_language(self, language_id: uuid.UUID):
        item = self.dao.get_item_by_language(language_id=language_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found")
        return item

    def delete_item(self, id: uuid.UUID):
        try:
            self.dao.delete_item(id)
        except DAOException as error:
            raise HTTPException(status_code=404, detail=str(error))

        return {"ok": True}

    def update_item(self, id: uuid.UUID, data):
        try:
            return self.dao.update_item(id=id, data=data)
        except DAOException as error:
            raise HTTPException(status_code=404, detail=error)
