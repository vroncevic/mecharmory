# -*- coding: UTF-8 -*-

'''
Module
    itransport.py
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
    Abstract protocol interface for stream transport adapters.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransport(Protocol):
    '''
        Defines low-level transport operations.
    '''

    def open(self, endpoint: str, baudrate: int) -> bool:
        '''Opens communication channel.'''

    def close(self) -> None:
        '''Closes active communication channel.'''

    def write_line(self, line: str) -> bool:
        '''Transmits single ASCII line.'''

    def read_line(self) -> str | None:
        '''Reads single ASCII line or returns None if no data ready.'''

    def is_open(self) -> bool:
        '''Checks whether connection channel is active.'''
