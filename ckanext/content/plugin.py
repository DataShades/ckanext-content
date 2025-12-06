from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.types as types

from ckanext.content.middleware import render_content_if_exists
import ckanext.content.helpers as content_helpers
from ckanext.content.interfaces import IContent


@toolkit.blanket.validators
@toolkit.blanket.config_declarations
@toolkit.blanket.actions
@toolkit.blanket.auth_functions
@toolkit.blanket.helpers
@toolkit.blanket.blueprints
class ContentPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(IContent, inherit=True)

    _content_schemas = None
    _content_presets = None

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "content")

        self._content_schemas = content_helpers.register_content_schemas()
        self._content_presets = content_helpers.register_content_presets()

    # IMiddleware
    def make_middleware(self, app: types.CKANApp, _) -> types.CKANApp:
        app.after_request(render_content_if_exists)
        return app

    # IContent
    def content_schemas(self) -> list[dict]:
        """
        Return content schemas.
        Schemas are loaded once during plugin initialization.
        """
        if self._content_schemas is None:
            self._content_schemas = content_helpers.register_content_schemas()
        return self._content_schemas

    def content_presets(self) -> list[dict]:
        """
        Return content presets.
        Presets are loaded once during plugin initialization.
        """
        if self._content_presets is None:
            self._content_presets = content_helpers.register_content_presets()
        return self._content_presets
