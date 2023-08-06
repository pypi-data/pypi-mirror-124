from dataclasses import dataclass
from enum import Enum
import re
from token import STRING
from typing import Union

__version__ = '0.1.2'


# https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
STR_PREFIXES = {'r', 'u', 'R', 'U', 'f', 'F', 'fr', 'Fr', 'fR', 'FR', 'rf', 'rF', 'Rf', 'RF'}
BYTES_PREFIXES = {'b', 'B', 'br', 'Br', 'bR', 'BR', 'rb', 'rB', 'Rb', 'RB'}
_prefixes = '|'.join(STR_PREFIXES | BYTES_PREFIXES)

STR_LITERAL_REGEX = re.compile(rf'''
    ^
    (?P<prefix>{_prefixes})?
    (?P<quotechar>'{{3}}|"{{3}}|'|")
    (?P<body>.*)
    (?P=quotechar)
    $
''', flags=re.VERBOSE | re.DOTALL)


@dataclass
class EscapeStyle:
    type: type
    human: str
    regex: Union[re.Pattern, str]

    def __post_init__(self):
        if self.type not in {str, bytes}:
            raise ValueError(f"Style.type only supports str or bytes, not {self.type}")
        if not isinstance(self.regex, re.Pattern):
            self.regex = re.compile(self.regex)

    def __str__(self):
        return f'{self.human}'

    def findall(self, text):
        return self.regex.findall(text)


class PluginError(Enum):
    ESC101 = EscapeStyle(str, r'\ooo', r'(?:\A|[^\\])(\\[0-7]{1,3})')
    ESC102 = EscapeStyle(str, r'\xhh', r'(?:\A|[^\\])(\\x[0-9a-fA-F]{2})')
    ESC103 = EscapeStyle(str, r'\uhhhh', r'(?:\A|[^\\])(\\u[0-9a-fA-F]{4})')
    ESC104 = EscapeStyle(str, r'\Uhhhhhhhh', r'(?:\A|[^\\])(\\U[0-9a-fA-F]{8})')
    ESC105 = EscapeStyle(str, r'\N{named}', r'(?:\A|[^\\])(\\N\{[a-zA-Z0-9 -]+\})')

    ESC201 = EscapeStyle(bytes, r'\ooo', r'(?:\A|[^\\])(\\[0-7]{1,3})')
    ESC202 = EscapeStyle(bytes, r'\xhh', r'(?:\A|[^\\])(\\x[0-9a-fA-F]{2})')

    @classmethod
    def get_for_type(cls, type):
        if type not in {str, bytes}:
            raise ValueError(f'{cls.__name__} only has errors for bytes or str, not {type.__class__.__name__}')
        for style in cls:
            if type is style.value.type:
                yield style


@dataclass
class StringLiteral:
    _PARSING_REGEX = STR_LITERAL_REGEX

    prefix: str = ''
    quotechar: str = '\''
    body: str = ''

    @classmethod
    def from_repr(cls, repr_string):
        match = cls._PARSING_REGEX.search(repr_string)
        assert match is not None, f"StringLiteral can't parse the given repr {repr_string!r}"
        return cls(**match.groupdict(default=''))  # prefix capture group is optional

    @classmethod
    def make_str(cls, body, raw=False):
        """
        Return a StringLiteral instance corresponding to a str with the given body.
        Used for testing.
        """
        return cls(body=body, prefix='r' if raw else '')

    @classmethod
    def make_bytes(cls, body, raw=False):
        """
        Return a StringLiteral instance corresponding to a bytes with the given body.
        Used for testing.
        """
        return cls(prefix='br' if raw else 'b', body=body)

    @property
    def type(self):
        return bytes if self.prefix in BYTES_PREFIXES else str

    @property
    def is_raw(self):
        return 'r' in self.prefix or 'R' in self.prefix

    @property
    def escapes(self):
        # TODO: calculate the line/column offset
        if self.is_raw:
            return

        for error in PluginError.get_for_type(self.type):
            for escape in error.value.findall(self.body):
                yield error, escape


class Plugin:
    name = 'flake8-escaping-style'
    version = __version__

    def __init__(self, tree, file_tokens):
        self._string_tokens = [token for token in file_tokens if token.type == STRING]

    def _make_error(self, token, style, escape):
        msg = f'{style.name} escape style {style.value.human} found in string literal: {escape}'
        return (*token.start, msg, False)

    def __iter__(self):
        for token in self._string_tokens:
            literal = StringLiteral.from_repr(token.string)
            for style, escape in literal.escapes:
                yield self._make_error(token, style, escape)
