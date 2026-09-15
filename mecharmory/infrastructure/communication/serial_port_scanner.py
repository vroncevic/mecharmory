# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner.py
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
    Utility for scanning available physical serial ports on the host system.
'''

from __future__ import annotations

from serial.tools.list_ports import comports

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortScanner:
    '''
        Scans host operating system for serial communication ports.

        It defines:

            :methods:
                | get_available_ports - Returns sorted list of device paths.
                | is_pico_device - Identifies Raspberry Pi Pico RP2040 VID/PID.
    '''

    @staticmethod
    def get_available_ports() -> list[str]:
        '''
            Scans and returns discovered serial port names.

            :return: List of device file paths, prioritizing Raspberry Pi Pico.
        '''
        ports: list[str] = []
        pico_ports: list[str] = []

        try:
            for p in comports():
                device: str = p.device
                desc: str = (p.description or '').lower()
                hwid: str = (p.hwid or '').lower()

                # RP2040 USB CDC vendor ID is 2e8a
                if '2e8a' in hwid or 'pico' in desc or 'raspberry' in desc:
                    pico_ports.append(device)
                else:
                    ports.append(device)
        except (OSError, ValueError):
            pass

        return pico_ports + ports

    @staticmethod
    def is_pico_device(hwid: str) -> bool:
        '''
            Determines if hardware ID belongs to Raspberry Pi Pico.

            :param hwid: Hardware ID string.
            :return: True if Pico identified, False otherwise.
        '''
        return '2e8a' in hwid.lower()
