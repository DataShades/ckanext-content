from __future__ import annotations

from ckan.plugins.interfaces import Interface


class IContent(Interface):
    """
    Interface for providing content schemas and presets.
    """

    def content_schemas(self) -> list[dict]:
        """
        Return a list of content schema dictionaries.

        Each schema should be a dictionary with the following structure:
        {
            "content_type": "unique_type_name",
            "label": "Human Readable Label",
            "content_fields": [
                {
                    "field_name": "field1",
                    "label": "Field 1",
                    "validators": "not_empty unicode_safe",
                    ...
                },
                ...
            ]
        }

        Returns:
            list[dict]: List of content schema dictionaries
        """
        return []

    def content_presets(self) -> list[dict]:
        """
        Return a list of content preset dictionaries.

        Each preset should be a dictionary with the following structure:
        {
            "preset_name": "unique_preset_name",
            "values": {
                "form_snippet": "snippet_name",
                "validators": "default_validators",
                ...
            }
        }

        Returns:
            list[dict]: List of content preset dictionaries
        """
        return []
