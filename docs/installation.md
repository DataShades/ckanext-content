Activate your CKAN virtual environment:

```bash
. /usr/lib/ckan/default/bin/activate
```

Clone the source and install it on the virtualenv:

```bash
git clone https://github.com/Datashades/ckanext-content.git
cd ckanext-content
pip install -e .
```

Add `content` to the `ckan.plugins` setting in your CKAN config file:

```ini
ckan.plugins = ... content
```

Initialize `content` table in the DB:

```bash
ckan -c CKAN_CONFIG_PATH db upgrade -p content
```

Restart CKAN.

This will add default content types and presets. If you plan to register more types or extend templates, validation using ckanext-scheming, check the [Usage](usage.md) section.
