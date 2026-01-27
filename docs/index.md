**ckanext-content** is a modern and flexible content management extension for CKAN. It replaces legacy extensions like `ckanext-pages` and `ckanext-showcase` with a schema-driven, configurable solution that supports custom content types, translations, file uploads, templating, and URL aliasing.

It is highly recommended to use it with [ckanext-scheming](https://github.com/ckan/ckanext-scheming) installed in order to increase the amount of templates, field types, validators and presets you can use to build your Content pages. Check the [Usage](usage.md#extending-the-number-field-options) section for instructions.

![Main Content Screen](assets/main.png)

## Main features

**Custom Content Types** - Define multiple content types (e.g. Pages, Reports, Banners) via YAML configuration.

**Schema-Based Configuration** - Specify fields, form controls, validation, and rendering behavior with a scheming-like syntax.

**Alias Support** - Automatically generate or customize clean URLs for content entries. Configure a prefix (e.g. /blog/, /page/) and choose which field (e.g. title) becomes the alias slug.

**Custom Templates per Type** - Assign specific templates for reading and editing each content type.

**File Upload Support** - Attach files or images per content.

**Admin UI** - Manage all content and content types through the CKAN admin panel.

## Extra

**Menus** - To be able to add the created content or add sidebars to them, use [ckanext-menu](https://github.com/DataShades/ckanext-menu) to create custom menus and manipulate them from the UI.

**Files** - While ckanext-content has own files fields, you also instead can add consistent images, backgrounds, files and other resources that will be present on all content or specific content types by using [ckanext-media](https://github.com/DataShades/ckanext-media). This extension allows to create custom Media types or use Default types to upload and store different files from the UI and have them all in one place.

**Permissions** - By default, ckanext-content provides access control that grants full permissions to Sysadmins, while allowing anonymous users to view published content. For more granular access control, integrate with [ckanext-permissions](https://github.com/DataShades/ckanext-permissions) to define custom roles and permissions, enabling you to delegate content moderation and management to specific users or groups. See the [Permissions documentation](extra.md#permissions-and-access-control) for detailed setup instructions.

## When to use?

When you need more content on CKAN rather then only Datasets, Groups and Organizations (e.g. Pages, News, Blog etc.).

When you don't want to add additional APP that will be responsible to for the content (e.g. Pages, News, Blog etc.) and integrate it with CKAN using APIs.

When you want to attach for example Showcases for Datasets, you can create custom fields that will gather those and display on Dataset page or Show some content tiles on Homepage.
