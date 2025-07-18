# ckanext-content

**ckanext-content** is a modern and flexible content management extension for CKAN. It replaces legacy extensions like `ckanext-pages` and `ckanext-showcase` with a schema-driven, configurable solution that supports custom content types, translations, file uploads, templating, and URL aliasing.

It is highly recommended to use it with [ckanext-scheming](https://github.com/ckan/ckanext-scheming) installed in order to increase the amount of templates, field types, validators and presets you can use to build your Content pages. Check the [Usage](https://datashades.github.io/ckanext-content/usage/#extending-the-number-field-options) section for instructions.

![Main Content Screen](docs/assets/main.png)

Check full [documentation](https://datashades.github.io/ckanext-content/) for more information on how to use this extension.

## Main features

* **Custom Content Types** - Define multiple content types (e.g. Pages, Reports, Banners) via YAML configuration.

* **Schema-Based Configuration** - Specify fields, form controls, validation, and rendering behavior with a scheming-like syntax.

* **Alias Support** -  Automatically generate or customize clean URLs for content entries. Configure a prefix (e.g. /blog/, /page/) and choose which field (e.g. title) becomes the alias slug.

* **Custom Templates per Type** - Assign specific templates for reading and editing each content type.

* **File Upload Support** - Attach files or images per content.

* **Admin UI**: Manage all content and content types through the CKAN admin panel.


## Extra

**Menus** - To be able to add the created content or add sidebars to them, use [ckanext-menu](https://github.com/DataShades/ckanext-menu) to create custom menus and manipulate them from the UI.

**Files** - While ckanext-content has own files fields, you also instead can add consistent images, backgrounds, files and other resources that will be present on all content or specific content types by using [ckanext-media](https://github.com/DataShades/ckanext-media). This extension allows to create custom Media types or use Default types to upload and store different files from the UI and have them all in one place.

## When to use?

* When you need more content on CKAN rather then only Datasets, Groups and Organizations (e.g. Pages, News, Blog etc.).
* When you don't want to add additional APP that will be responsible to for the content (e.g. Pages, News, Blog etc.) and integrate it with CKAN using APIs.
* When you want to attach for example Showcases for Datasets, you can create custom fields that will gather those and display on Dataset page or Show some content tiles on Homepage.


## Installation

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv
```
git clone https://github.com/Datashades/ckanext-content.git
cd ckanext-content
pip install -e .
```
3. Add `content` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

3. Initialize `content` table in the DB.
```
ckan -c CKAN_CONFIG_PATH db upgrade -p content
```

4. Restart CKAN

This will add default content types and presets. If you plan to register more types or extend templates, validation using ckanext-scheming, check the Usage section in the documentation.

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
