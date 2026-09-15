# -*- coding: UTF-8 -*-

'''
Module
    iarm_storage_service.py
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
    Abstract protocol interface for arm storage and file persistence.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArmStorageService(Protocol):
    '''
        Protocol for storing and loading robot configurations and motion sequence files.

        It defines:

            :methods:
                | is_initialized - Checks if the storage service is initialized.
                | save_config - Serializes configuration data dictionary to target JSON file.
                | load_config - Deserializes configuration data dictionary from JSON file.
                | save_text_file - Writes string content to destination file.
                | load_text_file - Reads string content from source file.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the storage service is initialized.

            :return: True if initialized, False otherwise.
        '''

    def save_config(self, data: dict[str, object], filepath: str) -> None:
        '''
            Serializes configuration data dictionary to target JSON file.

            :param data: Dictionary containing configuration parameters.
            :param filepath: Target destination file path.
        '''

    def load_config(self, filepath: str) -> dict[str, object]:
        '''
            Deserializes configuration data dictionary from JSON file.

            :param filepath: Source JSON file path.
            :return: Dictionary containing loaded configuration parameters.
        '''

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes string content to destination file.

            :param content: Text content to write.
            :param filepath: Destination file path.
        '''

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads string content from source file.

            :param filepath: Source file path.
            :return: File text content string.
        '''
