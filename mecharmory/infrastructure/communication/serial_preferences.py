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

from os.path import expanduser
from pathlib import Path
from typing import Final

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.exceptions import ATSValueError, ATSTypeError

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
        Manages loading and saving serial connection preferences to disk using ats_utilities.

        It defines:

            :attributes:
                | PREFS_FILE_PATH - Default storage path for preferences JSON file.
                | KEY_PORT - Configuration key identifier for serial port path.
                | KEY_BAUDRATE - Configuration key identifier for serial baudrate.
                | DEFAULT_PORT - Fallback device port path.
                | DEFAULT_BAUDRATE - Fallback communication baudrate.
                | _filepath - Path to settings JSON file.
                | _context - Application ATS ContextBundle instance.
            :methods:
                | __init__ - Configures storage path and ATS context bundle.
                | load_preference - Returns stored port and baudrate tuple.
                | save_preference - Stores active port and baudrate.
    '''

    PREFS_FILE_PATH: Final[str] = '~/.mecharmory_prefs.json'
    KEY_PORT: Final[str] = 'port'
    KEY_BAUDRATE: Final[str] = 'baudrate'
    DEFAULT_PORT: Final[str] = '/dev/ttyACM0'
    DEFAULT_BAUDRATE: Final[int] = 115200

    _filepath: str
    _context: ContextBundle | None

    def __init__(
        self,
        context_bundle: ContextBundle | None = None,
        filepath: str | None = None
    ) -> None:
        '''
            Configures preferences storage path and ATS context bundle.

            :param context_bundle: Optional application ATS ContextBundle instance.
            :param filepath: Optional custom preferences file path.
        '''
        self._context = context_bundle
        self._filepath = filepath or expanduser(self.PREFS_FILE_PATH)

    def load_preference(self) -> tuple[str, int]:
        '''
            Loads saved configuration or default values using ATS Loader.

            :return: Tuple of (port, baudrate).
        '''
        target_path: Path = Path(expanduser(self._filepath)).resolve()

        if target_path.is_file() and self._context is not None:
            try:
                bundle = ConfigIOBundleFactory.create_bundle(
                    ConfigIOBundleOptions(
                        file_path=str(target_path),
                        context_bundle=self._context
                    )
                )
                loader = Loader(bundle)
                data = loader.load_configuration()

                if isinstance(data, dict):
                    return (
                        str(data.get(self.KEY_PORT, self.DEFAULT_PORT)),
                        int(data.get(self.KEY_BAUDRATE, self.DEFAULT_BAUDRATE))
                    )

            except (ATSValueError, ATSTypeError, OSError, ValueError):
                pass

        return (self.DEFAULT_PORT, self.DEFAULT_BAUDRATE)

    def save_preference(self, port: str, baudrate: int) -> None:
        '''
            Saves active port and baudrate to disk using ATS Storer.

            :param port: Device path string.
            :param baudrate: Communication speed integer.
        '''
        if self._context is None:
            return

        try:
            target_path: Path = Path(expanduser(self._filepath)).resolve()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.touch(exist_ok=True)

            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(target_path),
                    context_bundle=self._context
                )
            )
            storer = Storer(bundle)
            storer.store_configuration({
                self.KEY_PORT: port,
                self.KEY_BAUDRATE: baudrate
            })

        except (ATSValueError, ATSTypeError, OSError):
            pass
