# -*- coding: UTF-8 -*-

'''
Module
    serial_preferences_test.py
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
    Unit tests for SerialPreferences persistence helper.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from mecharmory.infrastructure.communication.iserial_preferences import (
    ISerialPreferences
)
from mecharmory.infrastructure.communication.serial_preferences import (
    SerialPreferences
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialPreferences(TestCase):
    '''
        Test cases for SerialPreferences persistence helper.

        It defines:

            :methods:
                | test_constants - Verifies class Final constant definitions.
                | test_protocol_conformance - Verifies structural ISerialPreferences conformance.
                | test_default_preference - Tests fallback when preferences file does not exist.
                | test_save_and_load_preference - Tests saving and reloading preferences to temporary file.
    '''

    def test_constants(self) -> None:
        '''Verifies class Final constant definitions.'''
        self.assertEqual(SerialPreferences.PREFS_FILE_PATH, '~/.mecharmory_prefs.json')
        self.assertEqual(SerialPreferences.KEY_PORT, 'port')
        self.assertEqual(SerialPreferences.KEY_BAUDRATE, 'baudrate')
        self.assertEqual(SerialPreferences.DEFAULT_PORT, '/dev/ttyACM0')
        self.assertEqual(SerialPreferences.DEFAULT_BAUDRATE, 115200)

    def test_protocol_conformance(self) -> None:
        '''Verifies structural ISerialPreferences conformance.'''
        ctx: ContextBundle = ContextBundleFactory.create_bundle()
        prefs = SerialPreferences(context_bundle=ctx)
        self.assertIsInstance(prefs, ISerialPreferences)

    def test_default_preference(self) -> None:
        '''Tests fallback when preferences file does not exist.'''
        ctx: ContextBundle = ContextBundleFactory.create_bundle()
        prefs = SerialPreferences(
            context_bundle=ctx,
            filepath='/tmp/non_existent_mecharmory_prefs_test_xyz.json'
        )
        port, baud = prefs.load_preference()
        self.assertEqual(port, SerialPreferences.DEFAULT_PORT)
        self.assertEqual(baud, SerialPreferences.DEFAULT_BAUDRATE)

    def test_save_and_load_preference(self) -> None:
        '''Tests saving and reloading preferences to temporary file.'''
        with NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            ctx: ContextBundle = ContextBundleFactory.create_bundle()
            prefs = SerialPreferences(
                context_bundle=ctx,
                filepath=tmp_path
            )
            prefs.save_preference('/dev/ttyUSB0', 57600)
            port, baud = prefs.load_preference()
            self.assertEqual(port, '/dev/ttyUSB0')
            self.assertEqual(baud, 57600)
        finally:
            if exists(tmp_path):
                remove(tmp_path)


if __name__ == '__main__':
    main()
