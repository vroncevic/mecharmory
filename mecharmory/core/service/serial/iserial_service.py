# -*- coding: UTF-8 -*-

'''
Module
    iserial_service.py
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
    Interface protocol for serial communication service managing worker lifecycle and dispatch.
'''

from __future__ import annotations

from typing import Callable, Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISerialService(Protocol):
    '''
        Protocol defining the interface for serial communication service.

        It defines:

            :methods:
                | is_initialized - Confirms operational readiness of serial service.
                | set_virtual_mode - Toggles virtual simulation versus hardware.
                | is_virtual_mode - Returns simulation flag.
                | connect - Establishes connection on active transport.
                | disconnect - Shuts down active connection.
                | send_line - Dispatches outgoing line to active transport.
                | is_connected - Returns connection state.
                | register_rx_callback - Adds callback for received lines.
                | register_status_callback - Adds callback for connection state.
    '''

    def is_initialized(self) -> bool:
        '''
            Confirms operational readiness of serial service.

            :return: True if transports are properly instantiated.
        '''

    def set_virtual_mode(self, enabled: bool) -> None:
        '''
            Configures virtual mode.

            :param enabled: True for virtual emulator, False for real hardware.
        '''

    def is_virtual_mode(self) -> bool:
        '''
            Returns active mode.

            :return: True if virtual, False if hardware.
        '''

    def connect(self, port: str, baudrate: int) -> bool:
        '''
            Opens selected transport connection and spawns worker.

            :param port: Device path or identifier.
            :param baudrate: Baud rate speed.
            :return: True on success, False on error.
        '''

    def disconnect(self) -> None:
        '''Terminates active connection and halts background worker.'''

    def send_line(self, line: str) -> bool:
        '''
            Dispatches command line through active transport.

            :param line: ASCII line content.
            :return: True if successfully written.
        '''

    def is_connected(self) -> bool:
        '''
            Checks active connection state.

            :return: True if active transport is open.
        '''

    def register_rx_callback(self, callback: Callable[[str], None]) -> None:
        '''
            Registers listener for incoming lines.

            :param callback: Handler function receiving line string.
        '''

    def register_status_callback(self, callback: Callable[[bool, str], None]) -> None:
        '''
            Registers listener for connection state transitions.

            :param callback: Handler function receiving state bool and description.
        '''
