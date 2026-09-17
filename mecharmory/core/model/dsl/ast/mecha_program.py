# -*- coding: UTF-8 -*-

'''
Module
    mecha_program.py
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
    Concrete implementation of Mecha DSL AST root program.
'''

from __future__ import annotations

from typing import Any, Iterator

from mecharmory.core.model.dsl.ast.mecha_instruction import MechaInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaProgram:
    '''
        Concrete representation of Mecha DSL program root.

        It defines:

            :attributes:
                | _instructions - Immutable sequence of parsed instruction nodes.
                | _variables - Symbol table mapping scalar names to numeric values.
                | _points - Symbol table mapping point names to 6-tuple angles.
            :methods:
                | __init__ - Initializes program with instructions and symbol tables.
                | instructions - Property retrieving instructions tuple.
                | variables - Property retrieving variables dictionary.
                | points - Property retrieving points dictionary.
                | get_variable - Retrieves variable value by name.
                | get_point - Retrieves 6-DOF posture tuple by name.
                | __len__ - Returns count of instructions.
                | __iter__ - Returns iterator over instructions.
    '''

    _instructions: tuple[MechaInstruction, ...]
    _variables: dict[str, float]
    _points: dict[str, tuple[float, float, float, float, float, float]]

    def __init__(
        self,
        instructions: tuple[MechaInstruction, ...],
        variables: dict[str, float] | None = None,
        points: dict[str, tuple[float, float, float, float, float, float]] | None = None
    ) -> None:
        '''
            Initializes AST program root.

            :param instructions: Immutable tuple of instruction nodes.
            :param variables: Optional symbol table for scalar variables.
            :param points: Optional symbol table for 6-DOF postures.
        '''
        self._instructions = instructions
        self._variables = dict(variables) if variables is not None else {}
        self._points = dict(points) if points is not None else {}

    @property
    def instructions(self) -> tuple[Any, ...]:
        '''
            Retrieves sequence of instructions.

            :return: Tuple of MechaInstruction instances.
        '''
        return self._instructions

    @property
    def variables(self) -> dict[str, float]:
        '''
            Retrieves declared scalar variables mapping.

            :return: Dictionary mapping variable names to float values.
        '''
        return self._variables

    @property
    def points(self) -> dict[str, tuple[float, float, float, float, float, float]]:
        '''
            Retrieves declared 6-DOF point postures mapping.

            :return: Dictionary mapping point names to 6-tuple angles.
        '''
        return self._points

    def get_variable(self, name: str) -> float | None:
        '''
            Retrieves scalar variable value by name.

            :param name: Variable identifier.
            :return: Float value or None if undeclared.
        '''
        return self._variables.get(name)

    def get_point(
        self, name: str
    ) -> tuple[float, float, float, float, float, float] | None:
        '''
            Retrieves 6-DOF posture point by name.

            :param name: Point identifier.
            :return: 6-tuple of joint angles or None if undeclared.
        '''
        return self._points.get(name)

    def __len__(self) -> int:
        '''
            Returns total instruction count.

            :return: Integer count.
        '''
        return len(self._instructions)

    def __iter__(self) -> Iterator[Any]:
        '''
            Returns iterator across program instructions.

            :return: Iterator yielding instruction instances.
        '''
        return iter(self._instructions)
