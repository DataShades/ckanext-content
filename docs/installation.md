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
