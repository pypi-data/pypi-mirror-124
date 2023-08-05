# -*- coding: utf-8 -*-
"""
    pygments.lexers.boa
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the Boa language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from testflows._core.contrib.pygments.lexer import RegexLexer, words
from testflows._core.contrib.pygments.token import String, Comment, Keyword, Name, Number, Text, \
    Operator, Punctuation

__all__ = ['BoaLexer']

line_re = re.compile('.*?\n')


class BoaLexer(RegexLexer):
    """
    Lexer for the `Boa <http://boa.cs.iastate.edu/docs/>`_ language.

    .. versionadded:: 2.4
    """
    name = 'Boa'
    aliases = ['boa']
    filenames = ['*.boa']

    reserved = words(
        ('input', 'output', 'of', 'weight', 'before', 'after', 'stop',
         'ifall', 'foreach', 'exists', 'function', 'break', 'switch', 'case',
         'visitor', 'default', 'return', 'visit', 'while', 'if', 'else'),
        suffix=r'\b', prefix=r'\b')
    keywords = words(
        ('bottom', 'collection', 'maximum', 'mean', 'minimum', 'set', 'sum',
         'top', 'string', 'int', 'bool', 'float', 'time', 'false', 'true',
         'array', 'map', 'stack', 'enum', 'type'), suffix=r'\b', prefix=r'\b')
    classes = words(
        ('Project', 'ForgeKind', 'CodeRepository', 'Revision', 'RepositoryKind',
         'ChangedFile', 'FileKind', 'ASTRoot', 'Namespace', 'Declaration', 'Type',
         'Method', 'Variable', 'Statement', 'Expression', 'Modifier',
         'StatementKind', 'ExpressionKind', 'ModifierKind', 'Visibility',
         'TypeKind', 'Person', 'ChangeKind'),
        suffix=r'\b', prefix=r'\b')
    operators = ('->', ':=', ':', '=', '<<', '!', '++', '||',
                 '&&', '+', '-', '*', ">", "<")
    string_sep = ('`', '\"')
    built_in_functions = words(
        (
            # Array functions
            'new', 'sort',
            # Date & Time functions
            'yearof', 'dayofyear', 'hourof', 'minuteof', 'secondof', 'now',
            'addday', 'addmonth', 'addweek', 'addyear', 'dayofmonth', 'dayofweek',
            'dayofyear', 'formattime', 'trunctoday', 'trunctohour', 'trunctominute',
            'trunctomonth', 'trunctosecond', 'trunctoyear',
            # Map functions
            'clear', 'haskey', 'keys', 'lookup', 'remove', 'values',
            # Math functions
            'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
            'ceil', 'cos', 'cosh', 'exp', 'floor', 'highbit', 'isfinite', 'isinf',
            'isnan', 'isnormal', 'log', 'log10', 'max', 'min', 'nrand', 'pow',
            'rand', 'round', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc',
            # Other functions
            'def', 'hash', 'len',
            # Set functions
            'add', 'contains', 'remove',
            # String functions
            'format', 'lowercase', 'match', 'matchposns', 'matchstrs', 'regex',
            'split', 'splitall', 'splitn', 'strfind', 'strreplace', 'strrfind',
            'substring', 'trim', 'uppercase',
            # Type Conversion functions
            'bool', 'float', 'int', 'string', 'time',
            # Domain-Specific functions
            'getast', 'getsnapshot', 'hasfiletype', 'isfixingrevision', 'iskind',
            'isliteral',
        ),
        prefix=r'\b',
        suffix=r'\(')

    tokens = {
        'root': [
            (r'#.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (reserved, Keyword.Reserved),
            (built_in_functions, Name.Function),
            (keywords, Keyword.Type),
            (classes, Name.Classes),
            (words(operators), Operator),
            (r'[][(),;{}\\.]', Punctuation),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'`(\\\\|\\`|[^`])*`', String),
            (words(string_sep), String.Delimeter),
            (r'[a-zA-Z_]+', Name.Variable),
            (r'[0-9]+', Number.Integer),
            (r'\s+?', Text),  # Whitespace
        ]
    }
