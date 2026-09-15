# -*- coding: UTF-8 -*-

'''
Module
    serial_listener_hub.py
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
    Listener registry and notification dispatcher for serial communication events.
'''

from __future__ import annotations

from typing import Callable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialListenerHub:
    '''
        Manages notification callbacks for received lines and connection status transitions.

        It defines:

            :attributes:
                | _rx_callbacks - List of handlers for received data lines.
                | _status_callbacks - List of handlers for connection status changes.
            :methods:
                | __init__ - Initializes empty callback lists.
                | register_rx_callback - Adds received line handler.
                | register_status_callback - Adds connection status handler.
                | notify_rx - Dispatches received line to registered listeners.
                | notify_status - Dispatches connection state change to registered listeners.
    '''

    _rx_callbacks: list[Callable[[str], None]]
    _status_callbacks: list[Callable[[bool, str], None]]

    def __init__(self) -> None:
        '''
            Initializes empty listener collections.
        '''
        self._rx_callbacks = []
        self._status_callbacks = []

    def register_rx_callback(self, callback: Callable[[str], None]) -> None:
        '''
            Registers callback for incoming received lines.

            :param callback: Handler receiving raw line string.
        '''
        self._rx_callbacks.append(callback)

    def register_status_callback(self, callback: Callable[[bool, str], None]) -> None:
        '''
            Registers callback for connection state changes.

            :param callback: Handler receiving connected flag and status description.
        '''
        self._status_callbacks.append(callback)

    def notify_rx(self, line: str) -> None:
        '''
            Dispatches received line to registered listeners.

            :param line: Raw ASCII line.
        '''
        for cb in self._rx_callbacks:
            try:
                cb(line)
            except Exception:
                pass

    def notify_status(self, connected: bool, message: str) -> None:
        '''
            Dispatches connection state to registered listeners.

            :param connected: Connection active flag.
            :param message: Status description string.
        '''
        for cb in self._status_callbacks:
            try:
                cb(connected, message)
            except Exception:
                pass
