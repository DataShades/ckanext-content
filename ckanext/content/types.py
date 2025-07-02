from __future__ import annotations

from typing import Any, TypedDict


class Content(TypedDict):
    id: str
    title: str
    alias: str
    type: str
    author: str
    created: str
    modified: str
    data: dict[str, Any]


class ContentRevision(TypedDict):
    id: str
    content_id: str
    title: str
    alias: str
    type: str
    author: str
    created: str
    modified: str
    data: dict[str, Any]
