# -*- coding: UTF-8 -*-

'''
Module
    imecha_instruction.py
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
    Defines abstract protocol IMechaInstruction for Mecha DSL AST nodes.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaInstruction(Protocol):
    '''
        Abstract protocol for an individual AST instruction node.

        It defines:

            :attributes:
                | command_type - MechaCommandType discriminator.
                | line_number - Source code line index.
                | raw_line - Original unmodified text line.
                | parameters - Extracted parameter arguments dictionary.
            :methods:
                | get_param - Retrieves named parameter with optional default fallback.
    '''

    @property
    def command_type(self) -> MechaCommandType:
        '''
            Retrieves instruction command type.

            :return: MechaCommandType enum member.
        '''

    @property
    def line_number(self) -> int:
        '''
            Retrieves source line index.

            :return: Positive integer line number.
        '''

    @property
    def raw_line(self) -> str:
        '''
            Retrieves raw line text.

            :return: Unmodified string line.
        '''

    @property
    def parameters(self) -> dict[str, object]:
        '''
            Retrieves mapping of argument parameters.

            :return: Dictionary mapping parameter names to parsed values.
        '''

    def get_param(self, name: str, default: object = None) -> object:
        '''
            Retrieves parameter value by name with fallback.

            :param name: Parameter key name.
            :param default: Fallback object if key is absent.
            :return: Parameter value or default.
        '''
