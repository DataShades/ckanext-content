from typing import cast
import six

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins.toolkit as tk
import ckan.logic as logic
from ckan import types
import ckan.model as model


from ckanext.content import utils, types as content_types
from ckanext.content.model.content import ContentModel


ValidationError = logic.ValidationError


def create_ckan_content(context, data_dict):
    schema = data_dict.get("schema")
    data = data_dict.get("form_data")
    user = context["user"]

    prepared_schema = utils.prepare_schema_validation(schema, data)
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


def update_ckan_content(context, data_dict):
    schema = data_dict.get("schema")
    data = data_dict.get("form_data")
    id = data_dict.get("id")

    data["id"] = id

    prepared_schema = utils.prepare_schema_validation(schema, data)

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

    ckan_content = ContentModel.get_by_id(id)

    if not ckan_content:
        raise logic.NotFound("No such Content.")

    content = ckan_content.update(data)

    return content


def delete_ckan_content(context: types.Context, data_dict: types.DataDict) -> bool:
    tk.check_access("delete_ckan_content", context, data_dict)

    snippet = cast(ContentModel, ContentModel.get_by_id(data_dict["id"]))

    snippet.delete()

    return True


@tk.side_effect_free
def ckan_content_list(
    context: types.Context, data_dict: types.DataDict
) -> list[content_types.Content]:
    tk.check_access("view_ckan_content_list", context, data_dict)

    return [snippet.dictize(context) for snippet in ContentModel.get_all()]
