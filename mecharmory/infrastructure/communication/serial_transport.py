# -*- coding: UTF-8 -*-

'''
Module
    serial_transport.py
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
    Hardware serial transport implementation using PySerial.
'''

from __future__ import annotations

from threading import Lock
from serial import Serial, SerialException

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransport:
    '''
        PySerial hardware port stream adapter.

        It defines:

            :attributes:
                | _serial - PySerial instance or None.
                | _lock - Mutex guarding I/O channel.
            :methods:
                | __init__ - Configures initial unallocated state.
                | open - Opens specified serial port and baudrate.
                | close - Shuts down serial handle cleanly.
                | write_line - Encodes and flushes line out.
                | read_line - Reads decoded line with timeout.
                | is_open - Queries active connectivity.
    '''

    _serial: Serial | None
    _lock: Lock

    def __init__(self) -> None:
        '''Initializes transport adapter.'''
        self._serial = None
        self._lock = Lock()

    def open(self, endpoint: str, baudrate: int) -> bool:
        '''
            Opens physical serial connection.

            :param endpoint: Device path (e.g. /dev/ttyACM0).
            :param baudrate: Communication speed (e.g. 115200).
            :return: True on success, False on error.
        '''
        self.close()
        try:
            with self._lock:
                self._serial = Serial(
                    port=endpoint,
                    baudrate=baudrate,
                    timeout=0.1,
                    write_timeout=0.5
                )
            return True
        except (SerialException, OSError, ValueError):
            self._serial = None
            return False

    def close(self) -> None:
        '''Closes active serial connection.'''
        with self._lock:
            if self._serial is not None:
                try:
                    if self._serial.is_open:
                        self._serial.close()
                except (SerialException, OSError):
                    pass
                finally:
                    self._serial = None

    def write_line(self, line: str) -> bool:
        '''
            Transmits single ASCII line.

            :param line: ASCII string without trailing newline.
            :return: True if successfully written, False otherwise.
        '''
        with self._lock:
            if self._serial is None or not self._serial.is_open:
                return False

            payload: bytes = f'{line.strip()}\n'.encode('utf-8')
            try:
                self._serial.write(payload)
                self._serial.flush()
                return True
            except (SerialException, OSError):
                return False

    def read_line(self) -> str | None:
        '''
            Reads available line from hardware.

            :return: Decoded string or None.
        '''
        with self._lock:
            if self._serial is None or not self._serial.is_open:
                return None

            try:
                if self._serial.in_waiting > 0:
                    raw: bytes = self._serial.readline()
                    if raw:
                        return raw.decode('utf-8', errors='replace').strip()
            except (SerialException, OSError):
                return None

        return None

    def is_open(self) -> bool:
        '''
            Checks connectivity.

            :return: True if active, False otherwise.
        '''
        with self._lock:
            return self._serial is not None and self._serial.is_open
