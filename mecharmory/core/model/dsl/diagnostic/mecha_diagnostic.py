# -*- coding: UTF-8 -*-

'''
Module
    mecha_diagnostic.py
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
    Concrete implementation of diagnostic feedback message for Mecha DSL.
'''

from __future__ import annotations

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


class MechaDiagnostic:
    '''
        Concrete feedback item representing an error, warning, or notice in Mecha DSL.

        It defines:

            :attributes:
                | _line - 1-based source code line index.
                | _column - 1-based source column offset.
                | _message - Human-readable diagnostic description.
                | _severity - Diagnostic severity classification.
                | _code - Unique diagnostic rule identifier.
            :methods:
                | __init__ - Initializes diagnostic message object.
                | line - Property retrieving line number.
                | column - Property retrieving column offset.
                | message - Property retrieving message text.
                | severity - Property retrieving severity enum.
                | code - Property retrieving rule code.
                | formatted_message - Generates standardized display string.
    '''

    _line: int
    _column: int
    _message: str
    _severity: MechaDiagnosticSeverity
    _code: str

    def __init__(
        self,
        line: int,
        column: int,
        message: str,
        severity: MechaDiagnosticSeverity = MechaDiagnosticSeverity.ERROR,
        code: str = 'SYN001'
    ) -> None:
        '''
            Initializes diagnostic item.

            :param line: Source code line index.
            :param column: Source code column offset.
            :param message: Diagnostic description text.
            :param severity: Severity level enum member.
            :param code: Diagnostic error code.
        '''
        self._line = line
        self._column = column
        self._message = message
        self._severity = severity
        self._code = code

    @property
    def line(self) -> int:
        '''
            Retrieves diagnostic line number.

            :return: Line integer.
        '''
        return self._line

    @property
    def column(self) -> int:
        '''
            Retrieves diagnostic column offset.

            :return: Column integer.
        '''
        return self._column

    @property
    def message(self) -> str:
        '''
            Retrieves description message.

            :return: Diagnostic message string.
        '''
        return self._message

    @property
    def severity(self) -> MechaDiagnosticSeverity:
        '''
            Retrieves severity level.

            :return: MechaDiagnosticSeverity enum member.
        '''
        return self._severity

    @property
    def code(self) -> str:
        '''
            Retrieves diagnostic rule code.

            :return: Error classification string.
        '''
        return self._code

    def formatted_message(self) -> str:
        '''
            Formats diagnostic for UI console presentation.

            :return: Standardized string representation.
        '''
        return f'[{self._severity.value}] [{self._code}] L{self._line}:C{self._column} - {self._message}'
