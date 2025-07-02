from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context

from ckanext.content.model.content import ContentModel
from ckanext.content.model.content_revision import ContentRevisionModel
from ckanext.content import utils

ValidationError = logic.ValidationError

content = Blueprint("ckan_content", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateView(MethodView):
    def get(self, type):
        try:
            tk.check_access("create_ckan_content", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        schema = tk.h.get_content_schema(type)

        extra_vars = {
            "schema": schema,
            "data": {},
            "errors": {},
        }

        return tk.render("content/create.html", extra_vars=extra_vars)

    def post(self, type):
        try:
            tk.check_access("create_ckan_content", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        schema = tk.h.get_content_schema(type)
        data_dict = {
            "schema": schema,
            "form_data": form_data,
        }

        try:
            tk.get_action("create_ckan_content")(make_context(), data_dict)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "content/create.html",
                extra_vars={"data": form_data, "schema": schema, "errors": {}},
            )

        return tk.redirect_to("ckan_content.list")


class EditView(MethodView):
    def get(self, type: str, id: str):
        content = ContentModel.get_by_id(id)

        try:
            tk.check_access("edit_ckan_content", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not content:
            return tk.abort(404, "Page not found")

        schema = tk.h.get_content_schema(type)

        data = {
            "title": content.title,
            "alias": content.alias,
            "type": content.type,
            "state": content.state,
        }

        data.update(content.data)

        return tk.render(
            "content/edit.html",
            extra_vars={
                "type": type,
                "id": id,
                "data": data,
                "flat": utils.flatten_repeating_fields(data),
                "schema": schema,
                "errors": {},
            },
        )

    def post(self, type: str, id: str):
        try:
            tk.check_access("edit_ckan_content", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        for f_name, file in tk.request.files.items():
            correct_key = f_name.split("_content-")
            if file.filename and len(correct_key) and correct_key[1] == "upload":
                form_data[correct_key[0]] = file

        schema = tk.h.get_content_schema(type)
        data_dict = {
            "schema": schema,
            "form_data": form_data,
            "id": id,
        }

        try:
            tk.get_action("update_ckan_content")(make_context(), data_dict)
        except tk.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "content/edit.html",
                extra_vars={"data": form_data, "schema": schema, "errors": {}},
            )

        return tk.redirect_to("ckan_content.list", type=type, id=id)


class ReadView(MethodView):
    def _check_access(self, type: str, id: str):
        try:
            tk.check_access("read_ckan_content", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

    def get(self, type: str, id: str):
        content = ContentModel.get_by_id(id)

        if not content:
            return tk.abort(404, "Page not found")

        self._check_access(type, id)

        schema = tk.h.get_content_schema(type)

        template = tk.h.guess_content_type_snippet(type)
        return tk.render(
            template,
            extra_vars={
                "schema": schema,
                "type": type,
                "id": id,
                "content": content.dictize({}),
            },
        )


class ListView(MethodView):
    def get(self):
        try:
            tk.check_access("view_ckan_content_list", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        content = [content.dictize({}) for content in ContentModel.get_all()]

        return tk.render("content/list.html", extra_vars={"content": content})


class RevisionsListView(MethodView):
    def get(self, type, id):
        content = ContentModel.get_by_id(id)

        if not content:
            return tk.abort(404, "Page not found")

        try:
            tk.check_access("view_ckan_content_list", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        revisions = [
            rev.dictize({}) for rev in ContentRevisionModel.get_by_content_id(id)
        ]

        return tk.render(
            "content/revisions.html",
            extra_vars={"content": content, "revisions": revisions},
        )


class ReadRevisionView(MethodView):
    def _check_access(self, type: str, content_id: str, id: str):
        try:
            tk.check_access("read_ckan_content", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

    def get(self, type: str, content_id: str, id: str):
        revision = ContentRevisionModel.get_by_id(id)

        if not content:
            return tk.abort(404, "Page not found")

        self._check_access(type, content_id, id)

        schema = tk.h.get_content_schema(type)

        template = tk.h.guess_content_type_snippet(type)
        return tk.render(
            template,
            extra_vars={
                "schema": schema,
                "type": type,
                "id": content_id,
                "content": revision.dictize({}),
            },
        )


content.add_url_rule("/content/<type>/<id>", view_func=ReadView.as_view("read"))
content.add_url_rule(
    "/content/<type>/<id>/revisions",
    view_func=RevisionsListView.as_view("content_revisions"),
)
content.add_url_rule(
    "/content/<type>/<content_id>/revisions/<id>",
    view_func=ReadRevisionView.as_view("read_revision"),
)
content.add_url_rule("/content/<type>/create", view_func=CreateView.as_view("create"))
content.add_url_rule("/content/<type>/edit/<id>", view_func=EditView.as_view("edit"))
content.add_url_rule("/content/list", view_func=ListView.as_view("list"))
