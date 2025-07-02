from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.config.declaration.option import _validators_from_string


REDIS_CONTENT_SCHEMA_PREFIX = "ckan_content_schema_"
REDIS_CONTENT_PRESETS_KEY = "ckan_content_presets_global"


def get_content_redis_key(name: str) -> str:
    """
    Generate a Redis key by combining a prefix, the provided name, and a suffix.
    """
    return REDIS_CONTENT_SCHEMA_PREFIX + name


def get_content_presets_key() -> str:
    """
    Generate a Redis key by combining a prefix, the provided name, and a suffix.
    """
    return REDIS_CONTENT_PRESETS_KEY


def prepare_schema_validation(schema, data):
    fields = {}

    def _get_validators(field):
        validators_str = field.get("validators")

        if validators_str:
            validators = _validators_from_string(validators_str)
        else:
            validators = [
                tk.get_validator("ignore_missing"),
                tk.get_validator("unicode_safe"),
            ]

        # Make sure that ckanext-scheming validators work
        if "scheming_datasets" in tk.config.get("ckan.plugins"):
            for i, v in enumerate(validators):
                if getattr(v, "is_a_scheming_validator", False):
                    validators[i] = v(field, schema)

        return validators

    dataset_composite = {
        f["field_name"] for f in schema["content_fields"] if "repeating_subfields" in f
    }

    if dataset_composite:
        expand_form_composite(data, dataset_composite)

    for field in schema["content_fields"]:
        if field["field_name"] not in fields:
            field_name = field["field_name"]

            if "repeating_subfields" in field:
                subfield_schema = {}

                for rep_field in field["repeating_subfields"]:
                    rep_fieldname = rep_field["field_name"]
                    subfield_schema[rep_fieldname] = _get_validators(rep_field)

                fields[field_name] = subfield_schema
            else:
                validators = _get_validators(field)
                fields[field_name] = validators
    return fields


def expand_form_composite(data, fieldnames):
    """
    when submitting dataset/resource form composite fields look like
    "field-0-subfield..." convert these to lists of dicts
    """
    # if "field" exists, don't look for "field-0-subfield"
    fieldnames -= set(data)
    if not fieldnames:
        return
    indexes = {}
    for key in sorted(data):
        if "-" not in key:
            continue
        parts = key.split("-")
        if parts[0] not in fieldnames:
            continue
        if parts[1] not in indexes:
            indexes[parts[1]] = len(indexes)
        comp = data.setdefault(parts[0], [])
        parts[1] = indexes[parts[1]]
        try:
            try:
                comp[int(parts[1])]["-".join(parts[2:])] = data[key]
                del data[key]
            except IndexError:
                comp.append({})
                comp[int(parts[1])]["-".join(parts[2:])] = data[key]
                del data[key]
        except (IndexError, ValueError):
            pass  # best-effort only


def full_schema(schema):
    presets = tk.h.get_content_presets()

    merged_fields = []

    def _merge_with_presets(field):
        preset_name = field.get("preset")

        if preset_name:
            preset = [p for p in presets if p["preset_name"] == preset_name]

            if preset:
                return {**preset[0]["values"], **field}
        return field

    for field in schema["content_fields"]:
        field = _merge_with_presets(field)
        if "repeating_subfields" in field:
            for i, f in enumerate(field["repeating_subfields"]):
                if "preset" in f:
                    field["repeating_subfields"][i] = _merge_with_presets(f)

        merged_fields.append(field)

    schema["content_fields"] = merged_fields

    return schema


def parse_validators(validators_str):
    return [tk.get_validator(name) for name in validators_str.strip().split()]


def flatten_repeating_fields(data):
    flat_data = {}
    for key, value in data.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            for idx, item in enumerate(value):
                for sub_key, sub_value in item.items():
                    flat_data[f"{key}-{idx}-{sub_key}"] = sub_value
        else:
            flat_data[key] = value
    return flat_data
