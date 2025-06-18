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
