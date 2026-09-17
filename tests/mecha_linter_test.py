# -*- coding: UTF-8 -*-

'''
Module
    mecha_linter_test.py
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
    Unit tests for Mecha DSL semantic and kinematic linter.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)
from mecharmory.core.service.dsl.lexer.mecha_lexer import MechaLexer
from mecharmory.core.service.dsl.parser.mecha_parser import MechaParser
from mecharmory.core.service.dsl.linter.mecha_linter import MechaLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaLinter(TestCase):
    '''
        Test cases for MechaLinter kinematic and semantic analysis.

        It defines:

            :methods:
                | setUp - Prepares linter, parser, and lexer instances.
                | test_lint_valid_program - Tests clean script has no diagnostics.
                | test_lint_angle_out_of_bounds - Tests detecting angle beyond safe range.
                | test_lint_unknown_joint - Tests detecting invalid joint name.
                | test_lint_unknown_preset - Tests detecting invalid preset name.
                | test_lint_negative_wait - Tests detecting negative delay.
                | test_lint_invalid_speed - Tests detecting non-positive speed.
    '''

    _lexer: MechaLexer
    _parser: MechaParser
    _linter: MechaLinter

    def setUp(self) -> None:
        '''Prepares linter, parser, and lexer instances.'''
        self._lexer = MechaLexer()
        self._parser = MechaParser()
        self._linter = MechaLinter()

    def test_lint_valid_program(self) -> None:
        '''Tests clean script has no diagnostics.'''
        source = (
            'VAR S = 50.0\n'
            'POINT P = 90.0, 90.0, 90.0, 90.0, 90.0, 90.0\n'
            'SPEED S\n'
            'MOVE_P P\n'
            'MOVE_J BASE 120.0\n'
            'PRESET HOME\n'
            'WAIT_MS 200\n'
        )
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertEqual(len(diags), 0)

    def test_lint_angle_out_of_bounds(self) -> None:
        '''Tests detecting angle beyond safe range.'''
        # LIFT_1 valid range is 15.0 - 165.0 deg. 5.0 is out of bounds.
        source = 'MOVE_J LIFT_1 5.0\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertTrue(any(d.severity == MechaDiagnosticSeverity.ERROR for d in diags))
        self.assertTrue(any('outside safe range' in d.message for d in diags))

    def test_lint_unknown_joint(self) -> None:
        '''Tests detecting invalid joint name.'''
        source = 'MOVE_J INVALID_JOINT 90.0\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertTrue(any('Unknown joint identifier' in d.message for d in diags))

    def test_lint_unknown_preset(self) -> None:
        '''Tests detecting invalid preset name.'''
        source = 'PRESET NON_EXISTENT\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertTrue(any('Unknown preset name' in d.message for d in diags))

    def test_lint_negative_wait(self) -> None:
        '''Tests detecting negative delay.'''
        source = 'WAIT_MS -50\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertTrue(any('must be non-negative' in d.message for d in diags))

    def test_lint_invalid_speed(self) -> None:
        '''Tests detecting non-positive speed.'''
        source = 'SPEED -10.0\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        diags = self._linter.lint(program=program)
        self.assertTrue(any('must be positive' in d.message for d in diags))


if __name__ == '__main__':
    main()
