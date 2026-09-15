# -*- coding: UTF-8 -*-

'''
Module
    virtual_serial_transport_test.py
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
    Unit tests for VirtualSerialTransport adapter.
'''

from __future__ import annotations

from time import sleep
from unittest import TestCase, main

from mecharmory.infrastructure.communication.virtual_serial_transport import (
    VirtualSerialTransport
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualSerialTransport(TestCase):
    '''
        Test cases for VirtualSerialTransport adapter.

        It defines:

            :methods:
                | test_open_and_close - Tests connection lifecycle of virtual transport.
                | test_write_and_read - Tests sending commands and reading responses.
                | test_get_firmware - Tests accessing underlying emulator instance.
    '''

    def test_open_and_close(self) -> None:
        '''Tests connection lifecycle of virtual transport.'''
        trans = VirtualSerialTransport()
        self.assertFalse(trans.is_open())
        opened = trans.open('VIRTUAL', 115200)
        self.assertTrue(opened)
        self.assertTrue(trans.is_open())
        trans.close()
        self.assertFalse(trans.is_open())

    def test_write_and_read(self) -> None:
        '''Tests sending commands and reading responses.'''
        trans = VirtualSerialTransport()
        trans.open('VIRTUAL', 115200)
        try:
            # Drain startup banner
            while trans.read_line() is not None:
                pass
            written = trans.write_line('PING\n')
            self.assertTrue(written)
            sleep(0.05)
            response = trans.read_line()
            self.assertEqual(response, 'PONG')
        finally:
            trans.close()

    def test_get_firmware(self) -> None:
        '''Tests accessing underlying emulator instance.'''
        trans = VirtualSerialTransport()
        fw = trans.get_firmware()
        self.assertIsNotNone(fw)
        self.assertEqual(len(fw.get_angles()), 6)


if __name__ == '__main__':
    main()
