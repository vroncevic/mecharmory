# -*- coding: UTF-8 -*-

'''
Module
    imecha_diagnostic.py
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
    Defines abstract protocol IMechaDiagnostic for Mecha DSL analyzer feedback.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaDiagnostic(Protocol):
    '''
        Abstract protocol for validation and compilation diagnostic messages.

        It defines:

            :attributes:
                | line - 1-based source code line index.
                | column - 1-based source column offset.
                | message - Human-readable diagnostic description.
                | severity - Diagnostic severity level.
                | code - Diagnostic classification code identifier.
            :methods:
                | formatted_message - Generates standardized display string.
    '''

    @property
    def line(self) -> int:
        '''
            Retrieves diagnostic line number.

            :return: Line integer.
        '''

    @property
    def column(self) -> int:
        '''
            Retrieves diagnostic column offset.

            :return: Column integer.
        '''

    @property
    def message(self) -> str:
        '''
            Retrieves description message.

            :return: Diagnostic message string.
        '''

    @property
    def severity(self) -> MechaDiagnosticSeverity:
        '''
            Retrieves severity level.

            :return: MechaDiagnosticSeverity enum member.
        '''

    @property
    def code(self) -> str:
        '''
            Retrieves diagnostic error/rule code.

            :return: Error classification string.
        '''

    def formatted_message(self) -> str:
        '''
            Formats diagnostic for UI console presentation.

            :return: Standardized string representation.
        '''
