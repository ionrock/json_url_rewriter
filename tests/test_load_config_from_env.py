import json

from json_url_rewriter import config


class TestLoadConfigFromEnv(object):

    def test_no_config_with_no_env_vars(self):
        assert not config.load_from_environment({})

    def test_no_config_without_json_paths_to_check(self):
        assert not config.load_from_environment({config.KEYS: json.dumps([])})

    def test_config_loads_values_as_json(self):
        assert config.load_from_environment({config.KEYS: json.dumps({'hello': 'world'})})
