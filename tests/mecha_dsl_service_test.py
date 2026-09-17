# -*- coding: UTF-8 -*-

'''
Module
    mecha_dsl_service_test.py
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
    Unit tests for composite MechaDslService pipeline orchestrator.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.service.dsl.mecha_dsl_service import MechaDslService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaDslService(TestCase):
    '''
        Test cases for MechaDslService pipeline orchestration.

        It defines:

            :methods:
                | setUp - Prepares DSL service instance.
                | test_pipeline_valid_script - Tests atomic validate_and_compile on clean code.
                | test_pipeline_invalid_script - Tests that validation errors block compilation.
                | test_syntax_error_handling - Tests lexer error caught gracefully in lint.
    '''

    _service: MechaDslService

    def setUp(self) -> None:
        '''Prepares DSL service instance.'''
        self._service = MechaDslService()

    def test_pipeline_valid_script(self) -> None:
        '''Tests atomic validate_and_compile on clean code.'''
        source = (
            'VAR DELAY = 200\n'
            'HOME\n'
            'WAIT_MS DELAY\n'
            'MOVE_J BASE 100.0\n'
        )
        diags, cmds = self._service.validate_and_compile(source=source)
        self.assertEqual(len(diags), 0)
        self.assertEqual(cmds, ('HOME', 'WAIT 200', 'SET 0 100.00'))

    def test_pipeline_invalid_script(self) -> None:
        '''Tests that validation errors block compilation.'''
        # LIFT_1 = 5.0 is out of safe bounds [15.0, 165.0]
        source = 'MOVE_J LIFT_1 5.0\n'
        diags, cmds = self._service.validate_and_compile(source=source)
        self.assertGreater(len(diags), 0)
        self.assertEqual(len(cmds), 0)

    def test_syntax_error_handling(self) -> None:
        '''Tests lexer error caught gracefully in lint.'''
        diags = self._service.lint(source='MOVE_J @#$')
        self.assertGreater(len(diags), 0)
        self.assertEqual(diags[0].code, 'LEX001')


if __name__ == '__main__':
    main()
