# -*- coding: UTF-8 -*-

'''
Module
    imecha_program.py
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
    Defines abstract protocol IMechaProgram representing complete Mecha DSL AST root.
'''

from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable

from mecharmory.core.model.dsl.ast.imecha_instruction import IMechaInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaProgram(Protocol):
    '''
        Abstract protocol representing parsed Mecha DSL program root.

        It defines:

            :attributes:
                | instructions - Immutable sequence of parsed AST instruction nodes.
                | variables - Symbol table of scalar numeric variables.
                | points - Symbol table of defined 6-DOF posture points.
            :methods:
                | get_variable - Retrieves scalar variable value by identifier name.
                | get_point - Retrieves 6-DOF posture tuple by identifier name.
                | __len__ - Returns count of instructions in program.
                | __iter__ - Returns iterator over program instructions.
    '''

    @property
    def instructions(self) -> tuple[IMechaInstruction, ...]:
        '''
            Retrieves sequence of instructions.

            :return: Tuple of IMechaInstruction instances.
        '''

    @property
    def variables(self) -> dict[str, float]:
        '''
            Retrieves declared scalar variables mapping.

            :return: Dictionary mapping variable names to float values.
        '''

    @property
    def points(self) -> dict[str, tuple[float, float, float, float, float, float]]:
        '''
            Retrieves declared 6-DOF point postures mapping.

            :return: Dictionary mapping point names to 6-tuple angles.
        '''

    def get_variable(self, name: str) -> float | None:
        '''
            Retrieves scalar variable value by name.

            :param name: Variable identifier.
            :return: Float value or None if undeclared.
        '''

    def get_point(
        self, name: str
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Retrieves 6-DOF posture point by name.

            :param name: Point identifier.
            :return: 6-tuple of joint angles or None if undeclared.
        '''

    def __len__(self) -> int:
        '''
            Returns total instruction count.

            :return: Integer count.
        '''

    def __iter__(self) -> Iterator[IMechaInstruction]:
        '''
            Returns iterator across program instructions.

            :return: Iterator yielding instruction instances.
        '''
