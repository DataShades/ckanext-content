## Menus

**ckanext-content** itself, doesn't control or create menu items. In order to have managable Menus nagivation like Header, Footer or Sidebars on the Content pages, use [ckanext-menu](https://github.com/DataShades/ckanext-menu).


## Centralized files storage

**ckanext-content** has own file upload fields, but files that should be present across all Content or on any Content pages of specific type like Banners, Backgrounds, Files with infromation, use [ckanext-media](https://github.com/DataShades/ckanext-media) and add Media field for the Content where you can specify Media item Key that will be an reference to the actual Media File that can be updated independently from Content, but the changes will be reflected on Content pages.
