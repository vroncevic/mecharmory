# -*- coding: UTF-8 -*-

'''
Module
    mecha_parser.py
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
    Concrete implementation of Mecha DSL parser converting token stream into AST program.
'''

from __future__ import annotations

from typing import Any

from mecharmory.core.model.dsl.token.mecha_token import MechaToken
from mecharmory.core.model.dsl.token.mecha_token_type import MechaTokenType
from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType
from mecharmory.core.model.dsl.ast.mecha_instruction import MechaInstruction
from mecharmory.core.model.dsl.ast.mecha_program import MechaProgram
from mecharmory.core.service.dsl.parser.mecha_command_parser import MechaCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaParser:
    '''
        Concrete parser coordinating line token separation, symbol table resolution, and AST creation.

        It defines:

            :methods:
                | parse - Parses token stream into MechaProgram AST.
                | _split_lines - Groups token stream by NEWLINE delimiters.
                | _resolve_point_coords - Evaluates numeric or variable values into 6-DOF coordinate tuple.
    '''

    def parse(self, *, tokens: tuple[MechaToken, ...]) -> Any:
        '''
            Parses tokens into MechaProgram AST root.

            :param tokens: Tuple of MechaToken items.
            :return: MechaProgram AST instance.
        '''
        lines = self._split_lines(tokens)
        instructions: list[MechaInstruction] = []
        variables: dict[str, float] = {}
        points: dict[str, tuple[float, float, float, float, float, float]] = {}

        for line_tokens in lines:
            if not line_tokens:
                continue

            first_tok = line_tokens[0]
            cmd_name = first_tok.value.upper()
            if not hasattr(MechaCommandType, cmd_name):
                continue

            cmd_type = MechaCommandType(cmd_name)
            raw_line = ' '.join(t.value for t in line_tokens)
            params = MechaCommandParser.parse_line_tokens(cmd_type, line_tokens[1:])

            if cmd_type == MechaCommandType.VAR and 'name' in params and 'value' in params:
                try:
                    val_str = str(params['value'])
                    variables[str(params['name'])] = float(val_str)
                except ValueError:
                    pass

            elif cmd_type == MechaCommandType.POINT and 'name' in params and 'raw_values' in params:
                coords = self._resolve_point_coords(params['raw_values'], variables)
                if coords is not None:
                    points[str(params['name'])] = coords
                    params['coords'] = coords

            instructions.append(
                MechaInstruction(
                    command_type=cmd_type,
                    line_number=first_tok.line,
                    raw_line=raw_line,
                    parameters=params
                )
            )

        return MechaProgram(
            instructions=tuple(instructions),
            variables=variables,
            points=points
        )

    def _split_lines(self, tokens: tuple[MechaToken, ...]) -> list[list[MechaToken]]:
        '''
            Groups tokens into lines separated by NEWLINE and EOF.

            :param tokens: Flat token sequence.
            :return: List of token lists for each statement line.
        '''
        lines: list[list[MechaToken]] = []
        current: list[MechaToken] = []

        for tok in tokens:
            if tok.token_type in (MechaTokenType.NEWLINE, MechaTokenType.EOF):
                if current:
                    lines.append(current)
                    current = []
            else:
                current.append(tok)

        if current:
            lines.append(current)
        return lines

    def _resolve_point_coords(
        self,
        raw_values: Any,
        variables: dict[str, float]
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Evaluates raw point coordinate strings into float values.

            :param raw_values: Sequence of string representations.
            :param variables: Active variables symbol table.
            :return: 6-tuple of coordinates or None if invalid.
        '''
        if not isinstance(raw_values, list) or len(raw_values) < 6:
            return None

        parsed: list[float] = []
        for val_str in raw_values[:6]:
            val_upper = str(val_str).upper()
            if val_upper in variables:
                parsed.append(variables[val_upper])
            else:
                try:
                    parsed.append(float(val_str))
                except ValueError:
                    return None

        return (parsed[0], parsed[1], parsed[2], parsed[3], parsed[4], parsed[5])
