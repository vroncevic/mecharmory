# -*- coding: UTF-8 -*-

'''
Module
    imecha_lexer.py
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
    Defines abstract protocol IMechaLexer for Mecha DSL tokenization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.dsl.token.mecha_token import MechaToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaLexer(Protocol):
    '''
        Abstract protocol for Mecha DSL tokenization.

        It defines:

            :methods:
                | tokenize - Converts raw Mecha DSL source code into a tuple of tokens.
    '''

    def tokenize(self, *, source: str) -> tuple[MechaToken, ...]:
        '''
            Tokenizes source text into a stream of lexical tokens.

            :param source: Raw source text.
            :return: Immutable tuple of MechaToken instances.
        '''
