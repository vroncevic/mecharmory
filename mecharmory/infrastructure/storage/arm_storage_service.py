# -*- coding: UTF-8 -*-

'''
Module
    arm_storage_service.py
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
    Infrastructure storage adapter for robot configuration and file persistence.
'''

from __future__ import annotations

from pathlib import Path

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmStorageService:
    '''
        Infrastructure storage adapter handling JSON configuration and file I/O operations.
        Integrates ats_utilities Loader and Storer for JSON configuration management.

        It defines:

            :attributes:
                | _context - The ContextBundle for ATS configuration I/O operations.
            :methods:
                | __init__ - Initializes the arm storage service with context bundle.
                | is_initialized - Confirms storage service operational readiness.
                | save_config - Saves configuration dictionary to JSON file path.
                | load_config - Loads configuration dictionary from JSON file path.
                | save_text_file - Writes string content to file path using UTF-8.
                | load_text_file - Reads string content from file path using UTF-8.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes the arm storage service with application context bundle.

            :param context_bundle: ATS ContextBundle instance.
        '''
        self._context = context_bundle

    def is_initialized(self) -> bool:
        '''
            Confirms storage service operational readiness.

            :return: True if initialized with valid context.
        '''
        return self._context is not None

    def save_config(self, data: dict[str, object], filepath: str) -> None:
        '''
            Saves configuration dictionary to JSON file path using ATS Storer.

            :param data: Configuration dictionary to serialize.
            :param filepath: Destination file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.touch(exist_ok=True)

        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=str(target_path),
                context_bundle=self._context
            )
        )
        storer = Storer(bundle)
        storer.store_configuration(data)

    def load_config(self, filepath: str) -> dict[str, object]:
        '''
            Loads configuration dictionary from JSON file path using ATS Loader.

            :param filepath: Source JSON file path.
            :return: Loaded configuration dictionary, or empty dict if not found.
        '''
        target_path: Path = Path(filepath).resolve()

        if not target_path.is_file():
            return {}

        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=str(target_path),
                context_bundle=self._context
            )
        )
        loader = Loader(bundle)
        loaded_data = loader.load_configuration()

        if isinstance(loaded_data, dict):
            return loaded_data

        return {}

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes string content to file path using UTF-8 encoding.

            :param content: Text content to write.
            :param filepath: Destination file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads string content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''
        target_path: Path = Path(filepath).resolve()

        if not target_path.is_file():
            return ''

        with open(target_path, 'r', encoding='utf-8') as file_handle:
            return file_handle.read()
