from __future__ import annotations

from typing import cast
import six

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins.toolkit as tk
import ckan.logic as logic
from ckan import types
import ckan.model as model


from ckanext.content import utils, types as content_types
from ckanext.content.model.content import ContentModel
from ckanext.content.model.content_revision import ContentRevisionModel


ValidationError = logic.ValidationError


def create_ckan_content(context, data_dict):
    tk.check_access("create_ckan_content", context, data_dict)
    schema = data_dict.get("schema")
    data = data_dict.get("form_data")
    user = context["user"]

    prepared_schema = utils.prepare_schema_validation(schema, data)

    context["schema"] = schema

    result, errors = dict_fns.validate(data, prepared_schema, context)

    if errors:
        raise logic.ValidationError(errors)

    title = result.pop("title")
    alias = result.pop("alias")
    state = result.pop("state")

    data = {
        "title": title,
        "alias": alias,
        "state": state,
        "type": schema["content_type"],
        "data": result,
    }

    if user:
        user_obj = model.User.by_name(six.ensure_text(user))
        if not user_obj:
            raise logic.ValidationError({"author": [f"Missing Author"]})
        data["author"] = user_obj.id

    content = ContentModel.create(data)

    return content


def create_ckan_content_translation(context, data_dict):
    tk.check_access("create_ckan_content", context, data_dict)
    schema = data_dict.get("schema")
    data = data_dict.get("form_data")
    content_id = data_dict.get("content_id")
    lang = data_dict.get("lang")

    if not content_id:
        raise logic.ValidationError({"content_id": ["Missing Content ID"]})
    user = context["user"]

    original_fields = schema["content_fields"]
    for_translation_only = [
        field for field in original_fields if field.get("translatable")
    ]

    schema["content_fields"] = for_translation_only

    prepared_schema = utils.prepare_schema_validation(schema, data)

    context["schema"] = schema

    result, errors = dict_fns.validate(data, prepared_schema, context)

    if errors:
        raise logic.ValidationError(errors)

    if lang:
        content = ContentModel.get_by_id(content_id)

        if content:
            content.update_translation(lang, result)

    return result


def update_ckan_content(context, data_dict):
    tk.check_access("edit_ckan_content", context, data_dict)
    schema = data_dict.get("schema")
    data = data_dict.get("form_data")
    id = data_dict.get("id")

    data["id"] = id

    prepared_schema = utils.prepare_schema_validation(schema, data)

    context["schema"] = schema

    result, errors = dict_fns.validate(data, prepared_schema, context)

    if errors:
        raise logic.ValidationError(errors)

    if "__extras" in result:
        result.pop("__extras")

    title = result.pop("title")
    alias = result.pop("alias")
    state = result.pop("state")

    data = {
        "title": title,
        "alias": alias,
        "state": state,
        "type": schema["content_type"],
        "data": result,
    }

    ckan_content = ContentModel.get_by_id(id)

    if not ckan_content:
        raise logic.NotFound("No such Content.")

    revision_data = dict(ckan_content.dictize({}))
    revision_data["content_id"] = revision_data.pop("id")

    revision_data.pop("translations")
    ContentRevisionModel.create(revision_data)

    content = ckan_content.update(data)

    ContentRevisionModel.limit_revisions_amount(id)

    return content


def delete_ckan_content(
    context: types.Context, data_dict: types.DataDict
) -> bool:
    tk.check_access("delete_ckan_content", context, data_dict)

    content = cast(ContentModel, ContentModel.get_by_id(data_dict["id"]))

    if content:
        revisions = ContentRevisionModel.get_by_content_id(content.id)
        for revision in revisions:
            revision.delete()

    content.delete()

    return True


def delete_ckan_content_translation(
    context: types.Context, data_dict: types.DataDict
) -> bool:
    tk.check_access("delete_ckan_content", context, data_dict)

    lang = data_dict["lang"]

    content = cast(ContentModel, ContentModel.get_by_id(data_dict["id"]))

    if content and content.translations:
        content.delete_translation_key(lang)

    return True


@tk.side_effect_free
def ckan_content_list(
    context: types.Context, data_dict: types.DataDict
) -> list[content_types.Content]:
    tk.check_access("view_ckan_content_list", context, data_dict)

    return [content.dictize(context) for content in ContentModel.get_all()]


@tk.side_effect_free
def get_file_uploaded_url(context: types.Context, data_dict: types.DataDict):
    filename = data_dict.get("filename", "")

    path = "/uploads/content/" + filename

    return tk.h.url_for(path, qualified=True)


def get_content(context: types.Context, data_dict: types.DataDict):
    id = data_dict.get("id")
    if id:
        content = cast(ContentModel, ContentModel.get_by_id(data_dict["id"]))
        if content:
            return content
    return None
