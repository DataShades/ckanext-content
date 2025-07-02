from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from typing_extensions import Self
from typing import Any

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.model.types import make_uuid

from ckanext.content import types as content_types


class ContentModel(tk.BaseModel):
    __tablename__ = "content"

    id = sa.Column(sa.Text, primary_key=True, default=make_uuid)
    title = sa.Column(sa.Text, nullable=False)
    alias = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    data = sa.Column(MutableDict.as_mutable(JSONB))
    author = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.String, nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())

    @classmethod
    def get_by_id(cls, id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_alias(cls, alias: str) -> Self | None:
        return model.Session.query(cls).filter(cls.alias == alias).first()

    @classmethod
    def get_by_type(cls, type: str) -> list[Self]:
        return (
            model.Session.query(cls)
            .filter(cls.type == type)
            .order_by(cls.modified.desc())
            .all()
        )

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified.desc()).all()

    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        content = cls(**data_dict)

        model.Session.add(content)
        model.Session.commit()

        return content

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        model.Session.commit()

    def dictize(self, context: types.Context) -> content_types.Content:
        return content_types.Content(
            id=str(self.id),
            title=str(self.title),
            alias=str(self.alias),
            type=str(self.type),
            author=str(self.author),
            state=str(self.state),
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
            data=self.data,  # type: ignore
        )
