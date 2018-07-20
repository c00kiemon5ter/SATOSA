"""Configuration object to hold the proxy options and utils."""

import collections
import os

import yaml

from satosa.config import errors


def _as_env_key(key):
    env_key = _ENV_CONFIG_OPTION_TMPL.format(
            prefix=_ENV_CONFIF_PREFIX,
            key=key)
    return env_key


def _from_env(key):
    env_key = _as_env_key(key)
    env_value = os.environ.get(env_key)
    return env_key, env_value


def _identity(x):
    return x


def _parse_file(config_file):
    """Load config from yaml file.

    :type config_file: str
    :rtype: dict

    :param config_file: yaml configuration file to load.
    :return: Loaded config
    """
    try:
        with open(config_file) as f:
            data = f.read()
            config = yaml.safe_load(data)
    except (IOError, yaml.YAMLError) as e:
        raise errors.ParseFileError(config_file) from e
    else:
        return config


def _parse_items_by_type(values):
    parsed_values = [_parse_by_type(value) for value in values]
    return parsed_values


def _parse_by_type(value):
    value_type = type(value)

    try:
        value_parser = _parsers[value_type]
    except KeyError as e:
        raise errors.ParserLookupError(value) from e

    try:
        value_parsed = value_parser(value)
    except (TypeError, KeyError, ValueError) as e:
        raise errors.ParseError(value) from e
    else:
        return value_parsed


def _parse(configuration):
    options = {}

    param_config_parsed = _parse_by_type(configuration)
    for option, settings in CONFIG_OPTIONS.items():
        default_value = settings.default
        env_option, env_value = _from_env(option)
        param_value = param_config_parsed.get(option)
        value = \
            env_value if env_value is not None else     \
            param_value if param_value is not None else \
            default_value
        parser = settings.parser or _identity
        parsed_value = parser(value)
        options[option] = parsed_value

    configuration = _Config(**options)
    return configuration


def _validate(configuration):
    for option, settings in CONFIG_OPTIONS.items():
        value = getattr(configuration, option, None)
        if settings.required and value is None:
            raise errors.ValidationError(option, value)
    return configuration


def parse(configuration=None):
    """Parse and validate the configuration.

    The configuration can be given as a filename that will be loaded, a
    dictionary, or through the environment.

    :param configuration: the given configuration
    :type configuration: str|dict|NoneType
    :rtype: _Config
    """
    if configuration is None:
        env_option, env_value = _from_env(_CONFIG_KEY)
        configuration = env_value or _DEFAULT_CONFIG_FILE
    configuration = _parse(configuration)
    configuration = _validate(configuration)
    return configuration


class _Option(object):
    def __init__(self, required=False, default=None, parser=_identity):
        self.required = required
        self.default = default
        self.parser = parser


CONFIG_OPTIONS = {
    'BASE': _Option(required=True),
    'INTERNAL_ATTRIBUTES': _Option(
        required=True,
        parser=_parse_by_type),
    'BACKEND_MODULES': _Option(
        required=True,
        default=[],
        parser=_parse_items_by_type),
    'FRONTEND_MODULES': _Option(
        required=True,
        default=[],
        parser=_parse_items_by_type),
    'MICRO_SERVICES': _Option(
        default=[],
        parser=_parse_items_by_type),
    'COOKIE_STATE_NAME': _Option(default='SATOSA_COOKIE'),
    'STATE_ENCRYPTION_KEY': _Option(required=True),
    'USER_ID_HASH_SALT': _Option(required=True),
    # XXX stderr_handler = logging.StreamHandler(sys.stderr)
    # XXX stderr_handler.setLevel(logging.DEBUG)
    # XXX root_logger = logging.getLogger("")
    # XXX root_logger.addHandler(stderr_handler)
    # XXX root_logger.setLevel(logging.DEBUG)
    'LOGGING': _Option(default={}),
    'CUSTOM_PLUGIN_MODULE_PATHS': _Option(default=[]),
}

_Config = collections.namedtuple('Config', CONFIG_OPTIONS.keys())

_CONFIG_KEY = 'CONFIG'
_ENV_CONFIF_PREFIX = 'SATOSA_'
_ENV_CONFIG_OPTION_TMPL = '{prefix}{key}'
_DEFAULT_CONFIG_FILE = 'proxy_conf.yaml'

_parsers = {
    type(None): _identity,
    dict: _identity,
    str: _parse_file,
}
