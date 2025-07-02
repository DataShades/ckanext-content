from __future__ import annotations

import ckan.plugins.toolkit as tk


CONTENT_SCHEMAS = "ckanext.content.schemas"
CONTENT_PRESETS = "ckanext.content.presets"
CONTENT_FORM_SNIPPETS_PATH = "ckanext.content.form_snippets_path"
CONTENT_DISPLAY_SNIPPETS_PATH = "ckanext.content.display_snippets_path"


def content_get_content_schemas():
    return tk.config.get(CONTENT_SCHEMAS)


def content_get_content_presets():
    return tk.config.get(CONTENT_PRESETS)


def content_get_content_form_snippets_path():
    return tk.config.get(CONTENT_FORM_SNIPPETS_PATH)


def content_get_content_display_snippets_path():
    return tk.config.get(CONTENT_DISPLAY_SNIPPETS_PATH)
