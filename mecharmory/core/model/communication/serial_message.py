# -*- coding: UTF-8 -*-

'''
Module
    serial_message.py
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
    Data object representing a transmitted or received serial communication line.
'''

from __future__ import annotations

from dataclasses import dataclass
from time import strftime, localtime

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class SerialMessage:
    '''
        Represents a serial log message event.

        It defines:

            :attributes:
                | direction - Direction indicator ('TX' or 'RX').
                | text - ASCII content of the message.
                | timestamp - Human-readable time string.
            :methods:
                | create_tx - Factory method for outgoing transmission.
                | create_rx - Factory method for incoming reception.
    '''

    direction: str
    text: str
    timestamp: str

    @classmethod
    def create_tx(cls, text: str) -> SerialMessage:
        '''
            Builds a transmitted message entry.

            :param text: Commanded line text.
            :return: SerialMessage instance with current time.
        '''
        time_str: str = strftime('%H:%M:%S', localtime())
        return cls(direction='TX', text=text.strip(), timestamp=time_str)

    @classmethod
    def create_rx(cls, text: str) -> SerialMessage:
        '''
            Builds a received message entry.

            :param text: Device response line text.
            :return: SerialMessage instance with current time.
        '''
        time_str: str = strftime('%H:%M:%S', localtime())
        return cls(direction='RX', text=text.strip(), timestamp=time_str)
