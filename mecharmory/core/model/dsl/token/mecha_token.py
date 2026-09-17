# -*- coding: UTF-8 -*-

'''
Module
    mecha_token.py
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
    Defines immutable lexical token value object MechaToken.
'''

from __future__ import annotations

from dataclasses import dataclass

from mecharmory.core.model.dsl.token.mecha_token_type import MechaTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MechaToken:
    '''
        Immutable lexical token representing parsed source entity in Mecha DSL.

        It defines:

            :attributes:
                | token_type - MechaTokenType classification.
                | value - Raw string content matched by the lexer.
                | line - 1-based source line index.
                | column - 1-based source column offset.
    '''

    token_type: MechaTokenType
    value: str
    line: int
    column: int
