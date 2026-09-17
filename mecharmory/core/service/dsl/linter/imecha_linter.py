# -*- coding: UTF-8 -*-

'''
Module
    imecha_linter.py
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
    Defines abstract protocol IMechaLinter for static code analysis and kinematic validation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.dsl.ast.imecha_program import IMechaProgram
from mecharmory.core.model.dsl.diagnostic.imecha_diagnostic import IMechaDiagnostic

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaLinter(Protocol):
    '''
        Abstract protocol for Mecha DSL kinematic and syntactic linter.

        It defines:

            :methods:
                | lint - Validates program AST and generates diagnostic feedback items.
    '''

    def lint(
        self,
        *,
        program: IMechaProgram,
        model: IArmModel | None = None
    ) -> tuple[IMechaDiagnostic, ...]:
        '''
            Performs static analysis and kinematic boundary validation on AST program.

            :param program: IMechaProgram AST hierarchy.
            :param model: Optional IArmModel for physical calibration boundaries.
            :return: Immutable tuple of diagnostic feedback items.
        '''
