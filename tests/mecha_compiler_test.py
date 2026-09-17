# -*- coding: UTF-8 -*-

'''
Module
    mecha_compiler_test.py
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
    Unit tests for Mecha DSL compiler translating AST to firmware commands.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.service.dsl.lexer.mecha_lexer import MechaLexer
from mecharmory.core.service.dsl.parser.mecha_parser import MechaParser
from mecharmory.core.service.dsl.compiler.mecha_compiler import MechaCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaCompiler(TestCase):
    '''
        Test cases for MechaCompiler code generation.

        It defines:

            :methods:
                | setUp - Prepares compiler, parser, and lexer.
                | test_compile_move_j - Tests SET command generation.
                | test_compile_move_p_point - Tests SETP command generation from point.
                | test_compile_preset - Tests preset posture generation.
                | test_compile_gripper - Tests gripper open/close mapping to joint 5.
                | test_compile_wait - Tests WAIT meta-instruction.
    '''

    _lexer: MechaLexer
    _parser: MechaParser
    _compiler: MechaCompiler

    def setUp(self) -> None:
        '''Prepares compiler, parser, and lexer.'''
        self._lexer = MechaLexer()
        self._parser = MechaParser()
        self._compiler = MechaCompiler()

    def test_compile_move_j(self) -> None:
        '''Tests SET command generation.'''
        source = 'MOVE_J BASE 120.0\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmds = self._compiler.compile(program=program)
        self.assertEqual(cmds, ('SET 0 120.00',))

    def test_compile_move_p_point(self) -> None:
        '''Tests SETP command generation from point.'''
        source = (
            'POINT P = 90.0, 100.0, 80.0, 90.0, 90.0, 90.0\n'
            'MOVE_P P\n'
        )
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmds = self._compiler.compile(program=program)
        self.assertEqual(cmds, ('SETP 90.00 100.00 80.00 90.00 90.00 90.00',))

    def test_compile_preset(self) -> None:
        '''Tests preset posture generation.'''
        source = 'PRESET HOME\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmds = self._compiler.compile(program=program)
        self.assertEqual(cmds, ('SETP 90.00 90.00 90.00 90.00 90.00 90.00',))

    def test_compile_gripper(self) -> None:
        '''Tests gripper open/close mapping to joint 5.'''
        source = 'GRIPPER OPEN\nGRIPPER CLOSE\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmds = self._compiler.compile(program=program)
        self.assertEqual(cmds, ('SET 5 180.00', 'SET 5 0.00'))

    def test_compile_wait(self) -> None:
        '''Tests WAIT meta-instruction.'''
        source = 'WAIT_MS 350\n'
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse(tokens=tokens)
        cmds = self._compiler.compile(program=program)
        self.assertEqual(cmds, ('WAIT 350',))


if __name__ == '__main__':
    main()
