from __future__ import annotations

from typing import Any
import re

import ckan.plugins.toolkit as tk
import ckan.types as types
import ckan.lib.uploader as uploader
from ckan.lib.munge import munge_title_to_name

from ckanext.content.model.content import ContentModel


OneOf = tk.get_validator("OneOf")
ignore_missing = tk.get_validator("ignore_missing")
not_empty = tk.get_validator("not_empty")


def content_required(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    pure_key = key[0]
    fields = context["schema"]["content_fields"]

    field_settings = [field for field in fields if field["field_name"] == pure_key][0]

    if field_settings.get("required"):
        return not_empty
    return ignore_missing


def content_prepare_alias(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Set an alias if auto creation is on."""
    pure_key = key[0]

    fields = context["schema"]["content_fields"]

    field_settings = [field for field in fields if field["field_name"] == pure_key][0]
    if field_settings and field_settings.get("alias_autogenerate"):
        target = field_settings.get("alias_source_field")
        if target:
            prefix = field_settings.get("alias_prefix", "/")
            alias = prefix + munge_title_to_name(data[(target,)])
            data[key] = alias

    return


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

    raise tk.Invalid(f"Such alias '{data[key]}' already exist.")


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


def upload_file_to_storage(key, data, errors, context):
    file_data = data.get(key)

    if isinstance(file_data, str):
        return
    try:
        upload = uploader.get_uploader("content")
        upload.update_data_dict(data, key, key, "clear_upload")
        upload.upload(uploader.get_max_image_size())
    except (tk.ValidationError, OSError) as e:
        raise tk.Invalid(str(e))


def content_choices(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    pure_key = key[0]
    fields = context["schema"]["content_fields"]

    field = [field for field in fields if field["field_name"] == pure_key][0]

    if "choices" in field:
        return OneOf([c["value"] for c in field["choices"]])

    def validator(value):
        if value is tk.missing or not value:
            return value
        choices = tk.h.content_field_choices(field)
        for choice in choices:
            if value == choice["value"]:
                return value
        raise tk.Invalid(_('unexpected choice "%s"') % value)

    return validator
