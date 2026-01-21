from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context

from ckanext.content.model.content import ContentModel
from ckanext.content import utils

ValidationError = logic.ValidationError

content_translations = Blueprint("ckan_content_translations", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateTranslationView(MethodView):
    def get(self, type, content_id, lang):
        try:
            tk.check_access(
                "create_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        schema = tk.h.get_content_schema(type)

        content = ContentModel.get_by_id(content_id)

        if not content:
            return tk.abort(404, "Page not found")

        data = {
            "title": content.title,
            "alias": content.alias,
            "type": content.type,
            "state": content.state,
        }

        data.update(content.data)

        extra_vars = {
            "schema": schema,
            "data": data,
            "errors": {},
            "type": type,
            "content_id": content_id,
            "lang": lang,
        }

        return tk.render(
            "content/translations/create.html", extra_vars=extra_vars
        )

    def post(self, type, content_id, lang):
        try:
            tk.check_access(
                "create_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
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
            "content_id": content_id,
            "lang": lang,
            "type": type,
        }

        try:
            tk.get_action("create_ckan_content_translation")(
                make_context(), data_dict
            )
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "content/translations/create.html",
                extra_vars={"data": form_data, "schema": schema, "errors": {}},
            )

        return tk.redirect_to(
            "ckan_content_translations.list", type=type, content_id=content_id
        )


class TranslationEditView(MethodView):
    def get(self, type: str, content_id: str, lang: str):
        content = ContentModel.get_by_id(content_id)

        try:
            tk.check_access(
                "edit_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not content:
            return tk.abort(404, "Page not found")

        schema = tk.h.get_content_schema(type)

        translations = content.translations

        if not translations or not translations.get(lang):
            return tk.abort(404, "Page not found")

        data = translations[lang]

        return tk.render(
            "content/translations/edit.html",
            extra_vars={
                "type": type,
                "content_id": content_id,
                "data": data,
                "flat": utils.flatten_repeating_fields(data),
                "schema": schema,
                "errors": {},
                "lang": lang,
            },
        )

    def post(self, type: str, content_id: str, lang: str):
        try:
            tk.check_access(
                "edit_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
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
            if (
                file.filename
                and len(correct_key)
                and correct_key[1] == "upload"
            ):
                form_data[correct_key[0]] = file

        schema = tk.h.get_content_schema(type)
        data_dict = {
            "schema": schema,
            "form_data": form_data,
            "content_id": content_id,
            "lang": lang,
            "type": type,
        }

        try:
            tk.get_action("create_ckan_content_translation")(
                make_context(), data_dict
            )
        except tk.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "content/translations/edit.html",
                extra_vars={"data": form_data, "schema": schema, "errors": {}},
            )

        return tk.redirect_to(
            "ckan_content_translations.list", type=type, content_id=content_id
        )


class TranslationDeleteView(MethodView):
    def get(self, type: str, content_id: str, lang: str):
        content = ContentModel.get_by_id(content_id)

        try:
            tk.check_access(
                "delete_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not content:
            return tk.abort(404, "Page not found")

        return tk.render(
            "content/translations/delete.html",
            extra_vars={
                "type": type,
                "content_id": content_id,
                "lang": lang,
                "errors": {},
            },
        )

    def post(self, type: str, content_id: str, lang: str):
        try:
            tk.check_access(
                "delete_ckan_content",
                make_context(),
                {"id": content_id, "type": type},
            )
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        form_data = {"id": content_id, "lang": lang, "type": type}

        try:
            tk.get_action("delete_ckan_content_translation")(
                make_context(), form_data
            )
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "content/translations/delete.html",
                extra_vars={
                    "type": type,
                    "content_id": content_id,
                    "lang": lang,
                    "errors": {},
                    "form_data": form_data,
                },
            )

        return tk.redirect_to(
            "ckan_content_translations.list", type=type, content_id=content_id
        )


class TranslationsView(MethodView):
    def get(self, type: str, content_id: str):
        try:
            tk.check_access("view_ckan_content_list", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        content = tk.get_action("get_content")(
            make_context(), {"id": content_id}
        )

        if not content:
            return tk.abort(404, "Page not found")

        extra_vars = {
            "content": content,
            "locals": tk.h.get_locales_dict(),
            "type": type,
            "content_id": content_id,
        }

        return tk.render(
            "content/translations/list.html", extra_vars=extra_vars
        )


content_translations.add_url_rule(
    "/content/translations/<type>/<content_id>",
    view_func=TranslationsView.as_view("list"),
)
content_translations.add_url_rule(
    "/content/translation/<type>/<content_id>/<lang>/create",
    view_func=CreateTranslationView.as_view("create"),
)
content_translations.add_url_rule(
    "/content/translation/<type>/<content_id>/<lang>/edit",
    view_func=TranslationEditView.as_view("edit"),
)
content_translations.add_url_rule(
    "/content/translation/<type>/<content_id>/<lang>/delete",
    view_func=TranslationDeleteView.as_view("delete"),
)
