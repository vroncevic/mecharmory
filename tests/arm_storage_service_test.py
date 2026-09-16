# -*- coding: UTF-8 -*-

'''
Module
    arm_storage_service_test.py
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
    Unit tests for ArmStorageService adapter.
'''

from __future__ import annotations

from os import remove
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from mecharmory.infrastructure.storage.arm_storage_service import ArmStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmStorageService(TestCase):
    '''
        Test cases for ArmStorageService.

        It defines:

            :attributes:
                | _context - ATS ContextBundle for test operations.
            :methods:
                | setUp - Prepares test ATS context.
                | test_initialization - Tests service readiness flag.
                | test_save_and_load_config - Tests JSON configuration persistence.
                | test_save_and_load_text - Tests text file persistence.
                | test_load_nonexistent_files - Tests fallback on missing files.
    '''

    _context: ContextBundle

    def setUp(self) -> None:
        '''Prepares test ATS context.'''
        self._context = ContextBundleFactory.create_bundle()

    def test_initialization(self) -> None:
        '''Tests service readiness flag.'''
        storage = ArmStorageService(self._context)
        self.assertTrue(storage.is_initialized())

    def test_save_and_load_config(self) -> None:
        '''Tests JSON configuration persistence.'''
        storage = ArmStorageService(self._context)
        temp_file = NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()

        try:
            payload: dict[str, object] = {'name': 'TestArm', 'speed': 60.0}
            storage.save_config(payload, temp_file.name)
            loaded = storage.load_config(temp_file.name)
            self.assertEqual(loaded.get('name'), 'TestArm')
            self.assertEqual(loaded.get('speed'), 60.0)
        finally:
            remove(temp_file.name)

    def test_save_and_load_text(self) -> None:
        '''Tests text file persistence.'''
        storage = ArmStorageService(self._context)
        temp_file = NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.close()

        try:
            text = 'SET 0 90.0\nSET 1 45.0\n'
            storage.save_text_file(text, temp_file.name)
            loaded = storage.load_text_file(temp_file.name)
            self.assertEqual(loaded, text)
        finally:
            remove(temp_file.name)

    def test_load_nonexistent_files(self) -> None:
        '''Tests fallback on missing files.'''
        storage = ArmStorageService(self._context)
        fake_path = '/tmp/nonexistent_mecharmory_config_12345.json'
        self.assertEqual(storage.load_config(fake_path), {})
        self.assertEqual(storage.load_text_file(fake_path), '')


if __name__ == '__main__':
    main()
