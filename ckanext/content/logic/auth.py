from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

from ckanext.content.model.content import ContentModel
from ckanext.content.utils import (
    check_content_permission,
    is_permissions_enabled,
)


HIGHEST_PERMISSION = "administer_content"


def has_administer_permission(user: str | None) -> bool:
    """Check if the user has administer content permission.

    Args:
        user: The user to check permissions for
    Returns:
        bool: True if user has administer content permission, False otherwise
    """
    return check_content_permission(HIGHEST_PERMISSION, user, fallback=False)


def view_ckan_content_list(
    context: Context, data_dict: DataDict
) -> AuthResult:
    user = context.get("user")
    action = "view_content_list"

    if is_permissions_enabled():
        if has_administer_permission(user):
            return {"success": True}

        return {
            "success": check_content_permission(action, user, fallback=True)
        }

    return {"success": False}


def read_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    content_id = tk.get_or_bust(data_dict, "id")
    type = tk.get_or_bust(data_dict, "type")
    action = f"{type}_read_content" if type else "read_content"
    unpublished = (
        f"{type}_read_unpublished_content"
        if type
        else "read_unpublished_content"
    )

    content = ContentModel.get_by_id(content_id)

    if not content:
        return {"success": False}

    user = context.get("user")

    if is_permissions_enabled():
        if has_administer_permission(user):
            return {"success": True}

        if content and content.state != "active":
            return {
                "success": check_content_permission(
                    unpublished, user, fallback=True
                )
            }
        return {
            "success": check_content_permission(action, user, fallback=True)
        }

    if content and content.state != "active":
        return {"success": False}

    return {"success": True}


def create_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    user = context.get("user")
    type = tk.get_or_bust(data_dict, "type")
    action = f"{type}_create_content" if type else "create_content"

    if is_permissions_enabled():
        if has_administer_permission(user):
            return {"success": True}

        return {
            "success": check_content_permission(action, user, fallback=True)
        }

    return {"success": False}


def edit_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    user = context.get("user")
    type = tk.get_or_bust(data_dict, "type")
    action = f"{type}_edit_content" if type else "edit_content"

    if is_permissions_enabled():
        if has_administer_permission(user):
            return {"success": True}

        return {
            "success": check_content_permission(action, user, fallback=True)
        }

    return {"success": False}


def delete_ckan_content(context: Context, data_dict: DataDict) -> AuthResult:
    user = context.get("user")

    type = tk.get_or_bust(data_dict, "type")
    action = f"{type}_delete_content" if type else "delete_content"

    if is_permissions_enabled():
        if has_administer_permission(user):
            return {"success": True}

        return {
            "success": check_content_permission(action, user, fallback=True)
        }

    return {"success": False}


def administer_ckan_content(
    context: Context, data_dict: DataDict
) -> AuthResult:
    user = context.get("user")

    if has_administer_permission(user):
        return {"success": True}

    return {"success": False}
