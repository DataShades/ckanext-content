from __future__ import annotations

from flask import Response

import ckan.plugins.toolkit as tk
import ckan.types as types

from ckanext.content.model.content import ContentModel
from ckanext.content.views.content import ReadView, make_context


def render_content_if_exists(response: types.Response) -> types.Response:
    """Check if the page exists at the given url.

    This allows us to show the page without registering the blueprint.
    We do it only if the original response is a 404, and it means,
    that there's no blueprint at the given url.
    """
    if response.status_code != 404:
        return response

    path = tk.request.path

    if content := ContentModel.get_by_alias(path):
        # delete to reinitialize webassets
        delattr(tk.g, "_webassets")

        try:
            tk.check_access("read_ckan_content", make_context(), {"id": content.id})
        except tk.NotAuthorized:
            return response

        return Response(
            ReadView().get(str(content.type), str(content.id)),
            status=200,
            mimetype="text/html",
        )

    return response
