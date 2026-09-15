# -*- coding: UTF-8 -*-

'''
Module
    mecharmory_bundle_test.py
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
    Unit tests for Mecharmory bundle setup components and factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.setup.keys import MecharmoryBundleKeys
from mecharmory.setup.registry import MecharmoryBundleRegistry
from mecharmory.setup.factory import MecharmoryBundleFactory
from mecharmory.setup.bundle import MecharmoryBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMecharmoryBundle(TestCase):
    '''
        Test cases for Mecharmory bundle setup and factory.

        It defines:

            :methods:
                | test_keys_mapping - Tests dependency and option key mappings.
                | test_versions - Tests registry and factory version retrieval.
                | test_factory_bundle_creation - Tests complete system bundle assembly.
    '''

    def test_keys_mapping(self) -> None:
        '''Tests dependency and option key mappings.'''
        dep_map = MecharmoryBundleKeys.get_dependency_to_type()
        self.assertIn(MecharmoryBundleKeys.DEPENDENCY_BASE, dep_map)
        self.assertIn(MecharmoryBundleKeys.DEPENDENCY_SERVICE, dep_map)
        self.assertIn(MecharmoryBundleKeys.DEPENDENCY_GUI, dep_map)
        self.assertIn(MecharmoryBundleKeys.DEPENDENCY_CLI, dep_map)

        opt_map = MecharmoryBundleKeys.get_option_to_type()
        self.assertIn(MecharmoryBundleKeys.OPTION_CONFIG_FILE, opt_map)
        self.assertIn(MecharmoryBundleKeys.OPTION_LEN1, opt_map)

    def test_versions(self) -> None:
        '''Tests registry and factory version retrieval.'''
        self.assertEqual(MecharmoryBundleRegistry.get_version(), '1.0.0')
        self.assertEqual(MecharmoryBundleFactory.get_version(), '1.0.0')

    def test_factory_bundle_creation(self) -> None:
        '''Tests complete system bundle assembly.'''
        bundle: MecharmoryBundle = MecharmoryBundleFactory.create_bundle()
        self.assertIsNotNone(bundle.base)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.cli)
        self.assertTrue(bundle.service.is_initialized())
        self.assertTrue(bundle.gui.is_initialized())
        self.assertTrue(bundle.cli.is_initialized())

        bundle_dict = bundle.to_dict()
        self.assertIsInstance(bundle_dict, dict)
        self.assertIn('service', bundle_dict)


if __name__ == '__main__':
    main()
