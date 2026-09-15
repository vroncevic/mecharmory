# -*- coding: UTF-8 -*-

'''
Module
    serial_preferences.py
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
    Persistence helper storing recent serial communication settings.
'''

from __future__ import annotations

from os.path import expanduser, exists
from json import dumps, loads

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPreferences:
    '''
        Manages loading and saving serial connection preferences to disk.

        It defines:

            :attributes:
                | _filepath - Path to settings JSON file.
            :methods:
                | __init__ - Configures storage path in user directory.
                | load_preference - Returns stored port and baudrate tuple.
                | save_preference - Stores active port and baudrate.
    '''

    _filepath: str

    def __init__(self) -> None:
        '''Configures file path.'''
        self._filepath = expanduser('~/.mecharmory_prefs.json')

    def load_preference(self) -> tuple[str, int]:
        '''
            Loads saved configuration or default values.

            :return: Tuple of (port, baudrate).
        '''
        if exists(self._filepath):
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    data = loads(f.read())
                    return (
                        str(data.get('port', '/dev/ttyACM0')),
                        int(data.get('baudrate', 115200))
                    )
            except (OSError, ValueError):
                pass
        return ('/dev/ttyACM0', 115200)

    def save_preference(self, port: str, baudrate: int) -> None:
        '''
            Saves active port and baudrate to disk.

            :param port: Device path string.
            :param baudrate: Communication speed integer.
        '''
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                content: str = dumps({'port': port, 'baudrate': baudrate}, indent=2)
                f.write(content)
        except OSError:
            pass
