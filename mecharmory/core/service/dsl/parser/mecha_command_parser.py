# -*- coding: UTF-8 -*-

'''
Module
    mecha_command_parser.py
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
    Dedicated line-level parameter parser for Mecha DSL instructions.
'''

from __future__ import annotations

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


class MechaCommandParser:
    '''
        Extracts structured parameters from a single command's line tokens.

        It defines:

            :methods:
                | parse_line_tokens - Converts tokens following command keyword into parameter mapping.
                | parse_var_def - Extracts variable name and numeric value.
                | parse_point_def - Extracts point name and coordinate values.
    '''

    @classmethod
    def parse_line_tokens(
        cls,
        cmd_type: MechaCommandType,
        arg_tokens: list[MechaToken]
    ) -> dict[str, object]:
        '''
            Builds parameter dictionary from argument tokens.

            :param cmd_type: Identified command type.
            :param arg_tokens: Tokens following the command keyword.
            :return: Dictionary mapping parameter names to parsed values.
        '''
        match cmd_type:
            case MechaCommandType.VAR:
                return cls.parse_var_def(arg_tokens)
            case MechaCommandType.POINT:
                return cls.parse_point_def(arg_tokens)
            case _:
                return cls._parse_generic_arguments(arg_tokens)

    @classmethod
    def parse_var_def(cls, tokens: list[MechaToken]) -> dict[str, object]:
        '''
            Parses 'VAR <NAME> = <VALUE>' declaration.

            :param tokens: Tokens after VAR keyword.
            :return: Dictionary with 'name' and 'value'.
        '''
        params: dict[str, object] = {}
        filtered = [t for t in tokens if t.token_type != MechaTokenType.COMMA]
        if filtered:
            params['name'] = filtered[0].value.upper()
        # Find token after EQUALS if present
        for idx, tok in enumerate(filtered):
            if tok.token_type == MechaTokenType.EQUALS and idx + 1 < len(filtered):
                params['value'] = filtered[idx + 1].value
                break
        else:
            if len(filtered) > 1 and 'value' not in params:
                params['value'] = filtered[1].value
        return params

    @classmethod
    def parse_point_def(cls, tokens: list[MechaToken]) -> dict[str, object]:
        '''
            Parses 'POINT <NAME> = <J0>, <J1>, ...' declaration.

            :param tokens: Tokens after POINT keyword.
            :return: Dictionary with 'name' and 'raw_values'.
        '''
        params: dict[str, object] = {}
        if not tokens:
            return params
        params['name'] = tokens[0].value.upper()

        values: list[str] = []
        after_equals = False
        for tok in tokens[1:]:
            if tok.token_type == MechaTokenType.EQUALS:
                after_equals = True
                continue
            if tok.token_type == MechaTokenType.COMMA:
                continue
            if after_equals or len(tokens) > 2:
                values.append(tok.value)

        params['raw_values'] = values
        return params

    @classmethod
    def _parse_generic_arguments(cls, tokens: list[MechaToken]) -> dict[str, object]:
        '''
            Parses positional and keyword ('KEY=VAL') arguments.

            :param tokens: Argument token sequence.
            :return: Extracted parameters dictionary.
        '''
        params: dict[str, object] = {}
        positional: list[str] = []
        idx = 0
        filtered = [t for t in tokens if t.token_type != MechaTokenType.COMMA]

        while idx < len(filtered):
            tok = filtered[idx]
            if idx + 2 < len(filtered) and filtered[idx + 1].token_type == MechaTokenType.EQUALS:
                key = tok.value.lower()
                val = filtered[idx + 2].value
                params[key] = val
                idx += 3
            else:
                positional.append(tok.value)
                idx += 1

        if positional:
            params['args'] = positional
        return params
