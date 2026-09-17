# -*- coding: UTF-8 -*-

'''
Module
    mecha_parser_test.py
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
    Unit tests for Mecha DSL syntax parser.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType
from mecharmory.core.service.dsl.lexer.mecha_lexer import MechaLexer
from mecharmory.core.service.dsl.parser.mecha_parser import MechaParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaParser(TestCase):
    '''
        Test cases for MechaParser AST creation.

        It defines:

            :methods:
                | setUp - Prepares parser and lexer instances.
                | test_parse_empty - Tests parsing empty token stream.
                | test_parse_variables_and_points - Tests symbol table population.
                | test_parse_instructions - Tests extracting AST instruction nodes.
                | test_program_iteration - Tests len and iter on program.
    '''

    _lexer: MechaLexer
    _parser: MechaParser

    def setUp(self) -> None:
        '''Prepares parser and lexer instances.'''
        self._lexer = MechaLexer()
        self._parser = MechaParser()

    def test_parse_empty(self) -> None:
        '''Tests parsing empty token stream.'''
        tokens = self._lexer.tokenize(source='')
        program = self._parser.parse(tokens=tokens)
        self.assertEqual(len(program), 0)
        self.assertEqual(len(program.variables), 0)
        self.assertEqual(len(program.points), 0)

    def test_parse_variables_and_points(self) -> None:
        '''Tests symbol table population.'''
        source = (
            'VAR SPEED_FAST = 60.0\n'
            'POINT P_HOME = 90.0, 90.0, 90.0, 90.0, 90.0, 90.0\n'
            'MOVE_P P_HOME SPEED=SPEED_FAST\n'
        )
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        self.assertEqual(program.get_variable('SPEED_FAST'), 60.0)
        self.assertEqual(
            program.get_point('P_HOME'),
            (90.0, 90.0, 90.0, 90.0, 90.0, 90.0)
        )
        self.assertEqual(len(program), 3)

    def test_parse_instructions(self) -> None:
        '''Tests extracting AST instruction nodes.'''
        source = 'HOME\nWAIT_MS 300\nMOVE_J BASE 120.0\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmd_types = [instr.command_type for instr in program.instructions]
        self.assertEqual(
            cmd_types,
            [MechaCommandType.HOME, MechaCommandType.WAIT_MS, MechaCommandType.MOVE_J]
        )

    def test_program_iteration(self) -> None:
        '''Tests len and iter on program.'''
        source = 'HOME\nSTOP\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        self.assertEqual(len(program), 2)
        iter_types = [instr.command_type for instr in program]
        self.assertEqual(iter_types, [MechaCommandType.HOME, MechaCommandType.STOP])


if __name__ == '__main__':
    main()
