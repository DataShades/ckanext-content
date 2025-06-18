from typing import Any
import re

import ckan.plugins.toolkit as tk
import ckan.types as types

from ckanext.content.model.content import ContentModel


def content_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "content_required": content_required,
    }


def alias_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the given alias doesn't exist"""
    result = ContentModel.get_by_alias(data[key])

    if not result:
        return

    if data.get(("__extras",)) and data.get(("__extras",)).get("id"):
        current_content = ContentModel.get_by_id(data.get(("__extras",)).get("id"))
        if current_content and data[key] == current_content.alias:
            return

    raise tk.Invalid(f"Such alias already exists.")


def is_relative_path(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the given value is an relative path with leading slash"""
    value = data[key]

    if not isinstance(value, str):
        errors[key].append("Must be a string.")
        # return

    if not value.startswith("/") or value.startswith("//"):
        errors[key].append("Must start with a single slash (/) and not with //.")
        # return

    if not re.fullmatch(r"/[A-Za-z0-9][A-Za-z0-9_\-/]*", value):
        errors[key].append(
            'Path must start with a slash followed by a letter or digit, and contain only letters, digits, "-", or "_".'
        )

    if value.endswith("/"):
        errors[key].append('Should not end with "/".')
