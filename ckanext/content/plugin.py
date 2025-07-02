from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.types as types

from ckanext.content.middleware import render_content_if_exists
import ckanext.content.helpers as content_helpers


@toolkit.blanket.validators
@toolkit.blanket.config_declarations
@toolkit.blanket.actions
@toolkit.blanket.auth_functions
@toolkit.blanket.helpers
@toolkit.blanket.blueprints
class ContentPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "content")

        content_helpers.register_content_schemas()
        content_helpers.register_content_presets()

    # IMiddleware
    def make_middleware(self, app: types.CKANApp, _) -> types.CKANApp:
        app.after_request(render_content_if_exists)
        return app
