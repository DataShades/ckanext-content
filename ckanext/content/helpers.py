from __future__ import annotations

from flask import current_app
from jinja2 import TemplateNotFound
import os
import inspect
from typing import Any

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.common import _

from ckanext.content import utils, loader, config
from ckanext.content.types import Content
from ckanext.content.interfaces import IContent


def get_content_schemas():
    """
    Get all content schemas from all plugins implementing IContent.
    Schemas are cached at the plugin level, so files are read only once.
    """
    schemas = []
    for plugin in p.PluginImplementations(IContent):
        plugin_schemas = plugin.content_schemas()
        if plugin_schemas:
            schemas.extend(plugin_schemas)  # Use extend instead of assignment

    return schemas


def get_content_schema(name: str):
    schemas = get_content_schemas()
    schema = [schema for schema in schemas if schema["content_type"] == name]
    full_schema = utils.full_schema(schema[0]) if schema else {}
    return full_schema


def register_content_schemas() -> list[dict[str, Any]]:
    schemas_list = []

    schemas = config.content_get_content_schemas()

    for schema in schemas:
        module, file_name = schema.split(":", 1)

        try:
            # __import__ has an odd signature
            m = __import__(module, fromlist=[""])
        except ImportError:
            raise Exception("Cannot load module '%s'", module)

        p = os.path.join(os.path.dirname(inspect.getfile(m)), file_name)

        if os.path.exists(p):
            with open(p) as schema_file:
                schema = loader.load(schema_file)
                schemas_list.append(schema)

    return schemas_list


def get_schemas_types():
    schemas = get_content_schemas()

    return [{"label": s["label"], "type": s["content_type"]} for s in schemas]


def register_content_presets() -> list[dict[str, Any]]:
    presets = config.content_get_content_presets()

    gathered_presets = []
    for preset in presets:
        module, file_name = preset.split(":", 1)

        try:
            # __import__ has an odd signature
            m = __import__(module, fromlist=[""])
        except ImportError:
            raise Exception("Cannot load module '%s'", module)

        p = os.path.join(os.path.dirname(inspect.getfile(m)), file_name)

        if os.path.exists(p):
            with open(p) as preset_file:
                preset = loader.load(preset_file)
                gathered_presets.extend(preset["presets"])

    return gathered_presets


def get_content_presets():
    """
    Get all presets from all plugins implementing IContent.
    Presets are cached at the plugin level, so files are read only once.
    """
    presets = []
    for plugin in p.PluginImplementations(IContent):
        plugin_presets = plugin.content_presets()
        if plugin_presets:
            presets.extend(plugin_presets)  # Use extend instead of assignment

    return presets


def guess_snippet_from(name):
    env = current_app.jinja_env
    search_paths = config.content_get_content_form_snippets_path()

    for base in search_paths or []:
        path = base + name
        try:
            env.get_template(path)
            return path
        except TemplateNotFound:
            continue
    raise TemplateNotFound("Snippet '{name}' not found".format(name=name))


def guess_snippet_display(name):
    env = current_app.jinja_env
    search_paths = config.content_get_content_display_snippets_path()

    for base in search_paths or []:
        path = base + name
        try:
            env.get_template(path)
            return path
        except TemplateNotFound:
            continue
    raise TemplateNotFound("Snippet '{name}' not found".format(name=name))


def guess_content_type_snippet(type):
    env = current_app.jinja_env
    default_path = "content/display/"

    path = default_path + "content_" + type + ".html"
    try:
        env.get_template(path)
        return path
    except TemplateNotFound:
        return default_path + "content.html"


def uploaded_file_url(filename: str):
    return tk.get_action("get_file_uploaded_url")({}, {"filename": filename})


def content_field_required(field):
    if "required" in field:
        return field["required"]
    return "not_empty" in field.get("validators", "").split()


def content_field_choices(field):
    if "choices" in field:
        return field["choices"]
    if "choices_helper" in field:
        from ckantoolkit import h

        choices_fn = getattr(h, field["choices_helper"])
        return choices_fn(field)


def content_choices_label(choices, value):
    for c in choices:
        if c["value"] == value:
            return c.get("label", value)
    return value


def content_field_by_name(fields, name):
    for f in fields:
        if f.get("field_name") == name:
            return f


def content_translation_field(field, content: Content | dict[str, Any], default=None):
    type = "obj"
    text = ""
    if isinstance(content, dict):
        translations = content.get("translations")
        type = "dict"
    else:
        translations = content.translations

    if not translations:
        text = getattr(field, content) if type == "obj" else content.get(field, "")
    else:
        lang = tk.h.lang()
        if not lang in translations:
            text = getattr(field, content) if type == "obj" else content.get(field, "")
        else:
            data = translations[lang]
            if field in data and data[field]:
                text = data[field]

    if not text and default:
        text = default
    return text


def content_prepare_translation(content):
    translated = None
    if content:
        if not isinstance(content, dict):
            try:
                content = content.dictize({})
            except TypeError:
                return content

        data = content.get("data", {})

        if data:
            translated = {
                field: content_translation_field(field, content, value)
                for field, value in data.items()
            }

        if translated:
            content["data"] = translated

        content["title"] = content_translation_field(
            "title", content, default=content["title"]
        )

    return content
