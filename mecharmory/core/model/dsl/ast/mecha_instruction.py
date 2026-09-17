# -*- coding: UTF-8 -*-

'''
Module
    mecha_instruction.py
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
    Concrete implementation of AST instruction node for Mecha DSL.
'''

from __future__ import annotations

from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaInstruction:
    '''
        Concrete representation of an individual AST instruction in Mecha DSL.

        It defines:

            :attributes:
                | _command_type - MechaCommandType discriminator.
                | _line_number - 1-based source code line index.
                | _raw_line - Original unmodified text line.
                | _parameters - Extracted parameter arguments dictionary.
            :methods:
                | __init__ - Initializes instruction node with attributes.
                | command_type - Property retrieving command type.
                | line_number - Property retrieving line number.
                | raw_line - Property retrieving raw line text.
                | parameters - Property retrieving parameters dictionary.
                | get_param - Retrieves named parameter with optional default.
    '''

    _command_type: MechaCommandType
    _line_number: int
    _raw_line: str
    _parameters: dict[str, object]

    def __init__(
        self,
        command_type: MechaCommandType,
        line_number: int,
        raw_line: str,
        parameters: dict[str, object] | None = None
    ) -> None:
        '''
            Initializes AST instruction node.

            :param command_type: MechaCommandType enum instance.
            :param line_number: Source code line index.
            :param raw_line: Unmodified text line.
            :param parameters: Optional dictionary of parsed arguments.
        '''
        self._command_type = command_type
        self._line_number = line_number
        self._raw_line = raw_line
        self._parameters = parameters if parameters is not None else {}

    @property
    def command_type(self) -> MechaCommandType:
        '''
            Retrieves instruction command type.

            :return: MechaCommandType enum member.
        '''
        return self._command_type

    @property
    def line_number(self) -> int:
        '''
            Retrieves source line index.

            :return: Positive integer line number.
        '''
        return self._line_number

    @property
    def raw_line(self) -> str:
        '''
            Retrieves raw line text.

            :return: Unmodified string line.
        '''
        return self._raw_line

    @property
    def parameters(self) -> dict[str, object]:
        '''
            Retrieves mapping of argument parameters.

            :return: Dictionary mapping parameter names to parsed values.
        '''
        return self._parameters

    def get_param(self, name: str, default: object = None) -> object:
        '''
            Retrieves parameter value by name with fallback.

            :param name: Parameter key name.
            :param default: Fallback object if key is absent.
            :return: Parameter value or default.
        '''
        return self._parameters.get(name, default)
