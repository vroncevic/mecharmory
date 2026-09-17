# -*- coding: UTF-8 -*-

'''
Module
    mecha_lexer_test.py
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
    Unit tests for Mecha DSL lexical tokenizer.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.dsl.token.mecha_token_type import MechaTokenType
from mecharmory.core.service.dsl.lexer.mecha_lexer import MechaLexer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaLexer(TestCase):
    '''
        Test cases for MechaLexer tokenization.

        It defines:

            :methods:
                | setUp - Prepares lexer instance.
                | test_tokenize_empty - Tests tokenizing empty source string.
                | test_tokenize_commands_and_numbers - Tests command and numeric tokens.
                | test_tokenize_var_declaration - Tests VAR declaration tokenization.
                | test_tokenize_comment_ignored - Tests comments are filtered.
                | test_tokenize_invalid_char - Tests syntax error on illegal character.
    '''

    _lexer: MechaLexer

    def setUp(self) -> None:
        '''Prepares lexer instance.'''
        self._lexer = MechaLexer()

    def test_tokenize_empty(self) -> None:
        '''Tests tokenizing empty source string.'''
        tokens = self._lexer.tokenize(source='')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, MechaTokenType.EOF)

    def test_tokenize_commands_and_numbers(self) -> None:
        '''Tests command and numeric tokens.'''
        tokens = self._lexer.tokenize(source='MOVE_J BASE 90.0\nHOME')
        types = [t.token_type for t in tokens]
        self.assertIn(MechaTokenType.COMMAND, types)
        self.assertIn(MechaTokenType.IDENTIFIER, types)
        self.assertIn(MechaTokenType.NUMBER, types)
        self.assertIn(MechaTokenType.NEWLINE, types)
        self.assertEqual(tokens[-1].token_type, MechaTokenType.EOF)

    def test_tokenize_var_declaration(self) -> None:
        '''Tests VAR declaration tokenization.'''
        tokens = self._lexer.tokenize(source='VAR SPEED_SLOW = 30.0')
        vals = [t.value for t in tokens if t.token_type != MechaTokenType.EOF and t.token_type != MechaTokenType.NEWLINE]
        self.assertEqual(vals, ['VAR', 'SPEED_SLOW', '=', '30.0'])

    def test_tokenize_comment_ignored(self) -> None:
        '''Tests comments are filtered.'''
        tokens = self._lexer.tokenize(source='# Comment line\nHOME ; inline')
        types = [t.token_type for t in tokens]
        self.assertNotIn(MechaTokenType.COMMENT, types)
        cmd_tokens = [t for t in tokens if t.token_type == MechaTokenType.COMMAND]
        self.assertEqual(len(cmd_tokens), 1)
        self.assertEqual(cmd_tokens[0].value, 'HOME')

    def test_tokenize_invalid_char(self) -> None:
        '''Tests syntax error on illegal character.'''
        with self.assertRaises(ValueError):
            self._lexer.tokenize(source='MOVE_J @#$')


if __name__ == '__main__':
    main()
