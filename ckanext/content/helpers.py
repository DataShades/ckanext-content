from __future__ import annotations

from flask import current_app
from jinja2 import TemplateNotFound
import logging
import json
import os
import inspect
from typing import Any

from ckan.lib.redis import connect_to_redis, Redis
import ckan.plugins.toolkit as tk

from ckanext.content import utils, loader, config


def get_content_schemas():
    redis: Redis = connect_to_redis()

    keys = redis.keys(f"{utils.REDIS_CONTENT_SCHEMA_PREFIX}*")

    if not keys:
        keys = register_content_schemas()

    schemas = [json.loads(redis.get(k)) for k in keys]
    return schemas


def get_content_schema(name: str):
    redis: Redis = connect_to_redis()
    key = utils.get_content_redis_key(name)

    schema = json.loads(redis.get(key))

    full_schema = utils.full_schema(schema)
    return full_schema


def register_content_schemas() -> list[str] | None:
    keys = []
    redis: Redis = connect_to_redis()

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

                key = utils.get_content_redis_key(schema["content_type"])

                redis.set(key, json.dumps(schema), ex=604800)
                keys.append(key)

    return keys


def get_schemas_types():
    schemas = get_content_schemas()

    return [{"label": s["label"], "type": s["content_type"]} for s in schemas]


def register_content_presets() -> list[str] | None:
    redis: Redis = connect_to_redis()
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

    redis.set(utils.get_content_presets_key(), json.dumps(gathered_presets), ex=604800)

    return gathered_presets


def get_content_presets():
    redis: Redis = connect_to_redis()

    key = utils.get_content_presets_key()
    presets = redis.get(key)

    if not presets:
        presets = register_content_presets()
    else:
        presets = json.loads(presets)
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
        if f.get('field_name') == name:
            return f
