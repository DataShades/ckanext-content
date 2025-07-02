from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

from ckanext.content.model.content import ContentModel


def view_ckan_content_list(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


@tk.auth_allow_anonymous_access
def read_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    content_id = tk.get_or_bust(data_dict, "id")

    content = ContentModel.get_by_id(content_id)

    if not content:
        return {"success": False}

    if content and content.state != "active":
        return {"success": False}

    return {"success": True}


def create_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def edit_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def delete_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def administer_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}
