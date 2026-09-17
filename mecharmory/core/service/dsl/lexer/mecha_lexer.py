# -*- coding: UTF-8 -*-

'''
Module
    mecha_lexer.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    mecharmory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    mecharmory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Concrete implementation of Mecha DSL lexical tokenizer.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from typing import ClassVar

from mecharmory.core.model.dsl.token.mecha_token import MechaToken
from mecharmory.core.model.dsl.token.mecha_token_type import MechaTokenType
from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaLexer:
    '''
        Concrete lexer implementation converting Mecha DSL source into token stream.

        It defines:

            :attributes:
                | _TOKEN_REGEX - Compiled regular expression pattern matching DSL lexical entities.
                | _COMMAND_NAMES - Set of recognized canonical command keywords.
            :methods:
                | tokenize - Tokenizes raw source code into an immutable tuple of lexical tokens.
    '''

    _TOKEN_REGEX: ClassVar[Pattern[str]] = re_compile(
        r'(?P<COMMENT>[#;].*$)|'
        r'(?P<NUMBER>[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)|'
        r'(?P<STRING>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
        r'(?P<EQUALS>=)|'
        r'(?P<COMMA>,)|'
        r'(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)|'
        r'(?P<WHITESPACE>[^\S\n\r]+)|'
        r'(?P<MISMATCH>.)'
    )

    _COMMAND_NAMES: ClassVar[frozenset[str]] = frozenset(
        cmd.value for cmd in MechaCommandType
    )

    def tokenize(self, *, source: str) -> tuple[MechaToken, ...]:
        '''
            Tokenizes source text into a tuple of MechaToken instances.

            :param source: Raw source code string.
            :return: Immutable tuple of MechaToken tokens.
            :exceptions: ValueError if an unrecognized character is encountered.
        '''
        tokens: list[MechaToken] = []
        lines: list[str] = source.splitlines()

        for line_idx, line in enumerate(lines, start=1):
            line_has_tokens = False

            for match in self._TOKEN_REGEX.finditer(line):
                kind = match.lastgroup
                val = match.group()
                col = match.start() + 1

                if kind == 'WHITESPACE' or kind == 'COMMENT':
                    continue
                if kind == 'MISMATCH':
                    raise ValueError(
                        f'Syntax error: Unexpected character {val!r} at line {line_idx}, column {col}'
                    )

                token_type = self._resolve_token_type(kind, val)
                tokens.append(
                    MechaToken(
                        token_type=token_type,
                        value=val,
                        line=line_idx,
                        column=col
                    )
                )
                line_has_tokens = True

            if line_has_tokens:
                tokens.append(
                    MechaToken(
                        token_type=MechaTokenType.NEWLINE,
                        value='\n',
                        line=line_idx,
                        column=len(line) + 1
                    )
                )

        tokens.append(
            MechaToken(
                token_type=MechaTokenType.EOF,
                value='',
                line=len(lines) + 1,
                column=1
            )
        )
        return tuple(tokens)

    def _resolve_token_type(self, kind: str | None, val: str) -> MechaTokenType:
        '''
            Resolves lexical token classification.

            :param kind: Regex group name.
            :param val: Token text value.
            :return: MechaTokenType enum member.
        '''
        match kind:
            case 'NUMBER':
                return MechaTokenType.NUMBER
            case 'STRING':
                return MechaTokenType.STRING
            case 'EQUALS':
                return MechaTokenType.EQUALS
            case 'COMMA':
                return MechaTokenType.COMMA
            case 'IDENTIFIER':
                if val.upper() in self._COMMAND_NAMES:
                    return MechaTokenType.COMMAND
                return MechaTokenType.IDENTIFIER
            case _:
                return MechaTokenType.IDENTIFIER
