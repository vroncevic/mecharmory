# -*- coding: UTF-8 -*-

'''
Module
    serial_message_test.py
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
    Unit tests for SerialMessage value object.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.communication.serial_message import SerialMessage

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialMessage(TestCase):
    '''
        Test cases for SerialMessage value object.

        It defines:

            :methods:
                | test_create_tx - Tests creation of transmitted serial message.
                | test_create_rx - Tests creation of received serial message.
                | test_strip_whitespace - Tests stripping of trailing whitespace in message text.
    '''

    def test_create_tx(self) -> None:
        '''Tests creation of transmitted serial message.'''
        msg = SerialMessage.create_tx('SET 0 90.00')
        self.assertEqual(msg.direction, 'TX')
        self.assertEqual(msg.text, 'SET 0 90.00')
        self.assertIsInstance(msg.timestamp, str)
        self.assertGreater(len(msg.timestamp), 0)

    def test_create_rx(self) -> None:
        '''Tests creation of received serial message.'''
        msg = SerialMessage.create_rx('ACK: HOME')
        self.assertEqual(msg.direction, 'RX')
        self.assertEqual(msg.text, 'ACK: HOME')
        self.assertIsInstance(msg.timestamp, str)
        self.assertGreater(len(msg.timestamp), 0)

    def test_strip_whitespace(self) -> None:
        '''Tests stripping of trailing whitespace in message text.'''
        msg = SerialMessage.create_tx('  STATUS \r\n ')
        self.assertEqual(msg.text, 'STATUS')


if __name__ == '__main__':
    main()
