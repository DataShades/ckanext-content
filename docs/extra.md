## Menus

**ckanext-content** itself, doesn't control or create menu items. In order to have manageable Menus navigation like Header, Footer or Sidebars on the Content pages, use [ckanext-menu](https://github.com/DataShades/ckanext-menu).

## Centralized files storage

**ckanext-content** has own file upload fields, but files that should be present across all Content or on any Content pages of specific type like Banners, Backgrounds, Files with information, use [ckanext-media](https://github.com/DataShades/ckanext-media) and add Media field for the Content where you can specify Media item Key that will be a reference to the actual Media File that can be updated independently from Content, but the changes will be reflected on Content pages.

## Permissions and Access Control

By default, **ckanext-content** provides access control that grants full permissions to Sysadmins, while allowing anonymous users to view published content. For more granular access control, integrate with [ckanext-permissions](https://github.com/DataShades/ckanext-permissions) to define custom roles and permissions, enabling you to delegate content moderation and management to specific users or groups.

### Installation

Follow the [ckanext-permissions installation guide](https://github.com/DataShades/ckanext-permissions) to install and set up the extension. This includes:

Installing the extension.

Adding `permissions permissions_manager` to your plugins.

Running database migrations.

Initializing default roles.

### Configuration

After installing ckanext-permissions, add the content permissions group to your CKAN config file:

```ini
ckanext.permissions.permission_groups =
    ckanext.permissions:default_group.yaml
    ckanext.content:permissions/default_content_permissions.yaml
```

This registers the following permissions for content:

- `view_content_list` - View the list of content items (admin page)
- `read_content` - Read individual content items
- `create_content` - Create new content items
- `edit_content` - Edit existing content items
- `delete_content` - Delete content items
- `administer_content` - Full access to content administration

After updating the config, restart CKAN for the changes to take effect.

You can create your own permissions file from the Default, where you can add your custom content types to it in order to have permissions for them.
