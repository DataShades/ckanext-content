import pytest

from ckan.plugins import plugin_loaded


@pytest.mark.ckan_config("ckan.plugins", "content")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("content")
