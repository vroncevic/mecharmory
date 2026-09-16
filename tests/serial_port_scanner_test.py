# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner_test.py
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
    Unit tests for SerialPortScanner host discovery adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from mecharmory.infrastructure.communication.iserial_port_scanner import (
    ISerialPortScanner
)
from mecharmory.infrastructure.communication.serial_port_scanner import (
    SerialPortScanner
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialPortScanner(TestCase):
    '''
        Test cases for SerialPortScanner utility.

        It defines:

            :methods:
                | test_constants - Verifies class Final constant definitions.
                | test_protocol_conformance - Verifies structural ISerialPortScanner conformance.
                | test_is_pico_device - Tests identification of Raspberry Pi Pico hardware ID.
                | test_get_available_ports - Tests scanning and prioritizing Pico ports.
                | test_check_available_port - Tests checking port availability by name.
    '''

    def test_constants(self) -> None:
        '''Verifies class Final constant definitions.'''
        self.assertEqual(SerialPortScanner.RP2040_VID, '2e8a')
        self.assertEqual(SerialPortScanner.KEYWORD_PICO, 'pico')
        self.assertEqual(SerialPortScanner.KEYWORD_RASPBERRY, 'raspberry')

    def test_protocol_conformance(self) -> None:
        '''Verifies structural ISerialPortScanner conformance.'''
        scanner = SerialPortScanner()
        self.assertIsInstance(scanner, ISerialPortScanner)

    def test_is_pico_device(self) -> None:
        '''Tests identification of Raspberry Pi Pico hardware ID.'''
        self.assertTrue(SerialPortScanner.is_pico_device('USB VID:PID=2E8A:0005'))
        self.assertFalse(SerialPortScanner.is_pico_device('USB VID:PID=0403:6001'))

    @patch('mecharmory.infrastructure.communication.serial_port_scanner.comports')
    def test_get_available_ports(self, mock_comports: MagicMock) -> None:
        '''Tests scanning and prioritizing Pico ports.'''
        port_pico = MagicMock()
        port_pico.device = '/dev/ttyACM0'
        port_pico.description = 'Raspberry Pi Pico'
        port_pico.hwid = 'USB VID:PID=2E8A:0005'

        port_other = MagicMock()
        port_other.device = '/dev/ttyUSB0'
        port_other.description = 'FTDI Serial Adapter'
        port_other.hwid = 'USB VID:PID=0403:6001'

        mock_comports.return_value = [port_other, port_pico]
        ports = SerialPortScanner.get_available_ports()
        self.assertEqual(ports, ['/dev/ttyACM0', '/dev/ttyUSB0'])

    def test_check_available_port(self) -> None:
        '''Tests checking port availability by name.'''
        with patch.object(
            SerialPortScanner,
            'get_available_ports',
            return_value=['/dev/ttyACM0', '/dev/ttyUSB0']
        ):
            self.assertTrue(SerialPortScanner.check_available_port('/dev/ttyACM0'))
            self.assertTrue(SerialPortScanner.check_available_port('/dev/ttyUSB0'))
            self.assertFalse(SerialPortScanner.check_available_port('/dev/ttyACM1'))


if __name__ == '__main__':
    main()
