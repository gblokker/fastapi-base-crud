"""
Created on : Thursday, 16th October 2025 2:28:43 pm
Author: goof.blokker
Script type: A Eigen gebruik, B script, C tool, D complexe tool (lijstje uit ander document).
-----
Last Modified: Wednesday, 22nd October 2025 11:42:02 am
Modified By: goof.blokker
-----
Copyright 2025 - 2025 Antea Nederland B.V.
"""

import logging
from typing import Any, TypeVar
from weakref import WeakValueDictionary

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session  # type: ignore

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class CRUDBase[
    ModelType,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    ReadSchemaType: BaseModel,
]:
    """A generic CRUD base class for SQLAlchemy models."""

    _type_args: tuple[Any, ...] = ()
    _specialization_cache: WeakValueDictionary[tuple[Any, ...], type] = (
        WeakValueDictionary()
    )

    @classmethod
    def __class_getitem__(cls, params):
        """Create or reuse a specialized subclass carrying concrete type args."""
        if not isinstance(params, tuple):
            params = (params,)
        cached = cls._specialization_cache.get(params)
        if cached:
            return cached
        new_cls = type(
            f"[{','.join(getattr(p, '__name__', repr(p)) for p in params)}]",
            (cls,),
            {"_type_args": params},
        )
        cls._specialization_cache[params] = new_cls
        return new_cls

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """Validate type arguments on subclass creation, is not called when a subclass is not created."""
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "_type_args", ()):
            return
        if len(cls._type_args) != 4:
            raise ValueError("CRUDBase requires exactly four type arguments")
        model_type, create_schema_type, update_schema_type, get_schema_type = (
            cls._type_args
        )
        if not issubclass(model_type, DeclarativeBase):
            raise TypeError("ModelType must be a subclass of SQLAlchemy Base")
        if not issubclass(create_schema_type, BaseModel):
            raise TypeError("CreateSchemaType must be a subclass of Pydantic")
        if not issubclass(update_schema_type, BaseModel):
            raise TypeError("UpdateSchemaType must be a subclass of Pydantic")
        if not issubclass(get_schema_type, BaseModel):
            raise TypeError("ReadSchemaType must be a subclass of Pydantic")

    def __init__(self, db: Session, id_field_name: str):
        if not getattr(self, "_type_args", ()):
            raise TypeError(
                "CRUDBase must be instantiated with concrete type arguments"
            )
        self.model = self._type_args[0]
        if not hasattr(self.model, id_field_name):
            raise ValueError(
                f"Model {self.model.__name__} has no field '{id_field_name}'"
            )
        self.db = db
        self.id_field_name = id_field_name

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new instance of the model using data from the Pydantic schema."""
        logger.debug("create: input data=%r", obj_in.model_dump())
        obj: ModelType = self.model(**obj_in.model_dump())
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            identifier = getattr(obj, self.id_field_name, "unknown")
            logger.info("create: created model with id=%s", identifier)
            return obj
        except SQLAlchemyError as e:
            logger.error("create: commit failed: %s", e, exc_info=True)
            raise e

    def read(
        self,
        limit: int | None = None,
        offset: int | None = None,
        read_schema: ReadSchemaType | None = None,
    ) -> list[ModelType] | None:
        """Retrieve multiple model instances with optional pagination and optional filters from a Pydantic schema."""
        logger.debug("read: querying models with limit=%s, offset=%s", limit, offset)
        query = self.db.query(self.model)
        filters = []
        if read_schema:
            for field, value in read_schema.model_dump().items():
                if not hasattr(self.model, field):
                    continue
                if value is None:
                    continue
                col = getattr(self.model, field)
                if isinstance(value, list | tuple | set):
                    filters.append(col.in_(value))
                else:
                    filters.append(col == value)
        if filters:
            query = query.filter(*filters)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        results = query.all()
        logger.info("read: retrieved %d models", len(results))
        return results

    def read_by_id(self, id: Any) -> ModelType | None:
        """Retrieve a model instance by its primary key."""
        logger.debug("get: querying model with id=%s", id)
        db_obj: ModelType | None = (
            self.db.query(self.model)
            .filter(getattr(self.model, self.id_field_name) == id)
            .first()
        )
        if not db_obj:
            logger.warning("get: no model found with id=%s", id)
            return None
        logger.info("get: found model with id=%s", id)
        return db_obj

    def update(self, id: Any, obj_in: UpdateSchemaType) -> ModelType | None:
        """Update an existing model instance with data from the update schema.

        Args:
            id (Any): The value of the id field specified on initialization of the model instance to update.
            obj_in (UpdateSchemaType): The Pydantic schema instance containing updated data for the model.

        Returns:
            ModelType | None: The updated model instance if found, else None.

        """
        db_obj = self.read_by_id(id)
        if not db_obj:
            raise ValueError(f"update: no model found with id={id}")
        update_data = obj_in.model_dump(exclude_unset=True)
        if not any(hasattr(db_obj, field) for field, _ in update_data.items()):
            raise ValueError(f"update: no valid fields to update for id={id}")
        logger.debug("update: updating model id=%s with data=%r", id, update_data)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        try:
            self.db.commit()
            self.db.refresh(db_obj)
            logger.info("update: updated model with id=%s", id)
            updated = self.read_by_id(id)
            return updated
        except SQLAlchemyError as e:
            logger.error("update: commit failed for id=%s: %s", id, e, exc_info=True)
            raise e

    def delete(self, id: Any) -> ModelType | None:
        """Delete a model instance by its primary key."""
        db_obj = self.read_by_id(id)
        if not db_obj:
            logger.warning("delete: no model found with id=%s", id)
            return None
        try:
            self.db.delete(db_obj)  # type: ignore
            self.db.commit()
            logger.info("delete: deleted model with id=%s", id)
            return db_obj
        except SQLAlchemyError as e:
            logger.error("delete: commit failed for id=%s: %s", id, e, exc_info=True)
            raise e
