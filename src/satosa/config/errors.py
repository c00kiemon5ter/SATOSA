import satosa.exception


class ConfigurationError(satosa.exception.SATOSAError):
    """Generic configuration error."""


class ParserLookupError(ConfigurationError):
    """Error generating a parser."""

    def __init__(self, data):
        msg_tmpl = 'No suitable parser for: {type}:{data}'
        msg = msg_tmpl.format(type=type(data), data=data)
        super().__init__(msg)


class ParseError(ConfigurationError):
    """Error parsing configuration."""

    def __init__(self, data):
        msg_tmpl = 'Cannot parse configuration data: {type}:{data}'
        msg = msg_tmpl.format(type=type(data), data=data)
        super().__init__(msg)


class ParseFileError(ParseError):
    """Error while parsing a configuration file."""

    def __init__(self, filename):
        msg_tmpl = 'Cannot parse configuration file: {file}'
        msg = msg_tmpl.format(file=filename)
        super().__init__(msg)


class ValidationError(ConfigurationError):
    """Error while validating a configuration."""

    def __init__(self, option, value):
        msg_tmpl = 'Invalid value for option: {option}:{value}'
        msg = msg_tmpl.format(option=option, value=value)
        super().__init__(msg)
