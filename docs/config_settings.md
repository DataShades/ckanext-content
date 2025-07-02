**`ckanext.content.schemas`** - (list) Needed to be able to register custom content types besied the default types, example of Usage:
```
ckanext.content.schemas =
                ckanext.content:schemas/content/page.yaml
                ckanext.content:schemas/content/blog.yaml
```

**`ckanext.content.presets`** - (list) Need to be able to register additional presets (piece of field configurations that use multiple times across the schemas), example of Usage:
```
ckanext.content.presets =
                ckanext.content:schemas/content/presets.yaml
                ckanext.scheming:presets.json # Scheming presets is extension enabled
```

**`ckanext.content.form_snippets_path`** - (list) An ability to register additional paths to search from `form_snippets`, beside `ckanext.content` extension. Example of Usage:
```
ckanext.content.form_snippets_path =
                content/form_snippets/
                scheming/form_snippets/ # Scheming form_snippets is extension enabled
```

**`ckanext.content.display_snippets_path`** - (list) An ability to register additional paths to search from `display_snippets`, beside `ckanext.content` extension. Example of Usage:
```
ckanext.content.display_snippets_path =
                content/display_snippets/
                scheming/display_snippets/ # Scheming display_snippets is extension enabled
```
