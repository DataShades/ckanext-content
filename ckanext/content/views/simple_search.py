from flask import Blueprint
from typing import Any


import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.model as model
from ckan.types import Context
from ckan.lib.helpers import Page, pager_url

from ckanext.content.model.content import ContentModel


ValidationError = logic.ValidationError

simple_search = Blueprint("simple_search", __name__)

EXAMPLE_TYPE = "page"
EXAMPLE_LIMIT = 2


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


@simple_search.route("/content/search-example-1")
def simple_search_1():
    try:
        tk.check_access("administer_ckan_content", make_context(), {})
    except tk.NotAuthorized:
        return tk.abort(404, "Page not found")

    extra_vars: dict[str, Any] = {}
    extra_vars["q"] = q = tk.request.args.get("q", "")
    page = tk.h.get_page_number(tk.request.args)
    limit = EXAMPLE_LIMIT

    query = model.Session.query(ContentModel).filter_by(
        state="active", type=EXAMPLE_TYPE
    )

    if q:
        query = query.filter(ContentModel.title.ilike("%" + q.strip() + "%"))

    extra_vars["count"] = count = query.count()

    query = (
        query.order_by(ContentModel.modified.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    content = [item.dictize({}) for item in query]

    extra_vars["page"] = Page(
        collection=content,
        page=page,
        url=pager_url,
        item_count=count,
        items_per_page=limit,
    )
    extra_vars["page"].items = content

    return tk.render("content/examples/simple_search_1.html", extra_vars=extra_vars)
