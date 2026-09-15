# -*- coding: UTF-8 -*-

'''
Module
    cli_bundle_test.py
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
    Unit tests for CLI bundle setup components.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.infrastructure.cli.setup.keys import CLIBundleKeys
from mecharmory.infrastructure.cli.setup.registry import CLIBundleRegistry
from mecharmory.infrastructure.cli.setup.factory import CLIBundleFactory
from mecharmory.infrastructure.command.studio_command_definition import StudioCommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundle(TestCase):
    '''
        Test cases for CLI bundle setup.

        It defines:

            :methods:
                | test_keys_mapping - Tests dependency and option key mappings.
                | test_versions - Tests registry and factory version retrieval.
                | test_studio_command_definition - Tests CLI studio command definition.
    '''

    def test_keys_mapping(self) -> None:
        '''Tests dependency and option key mappings.'''
        dep_map = CLIBundleKeys.get_dependency_to_type()
        self.assertIn(CLIBundleKeys.DEPENDENCY_SERVICE, dep_map)
        self.assertIn(CLIBundleKeys.DEPENDENCY_PARSER, dep_map)
        self.assertIn(CLIBundleKeys.DEPENDENCY_COMMANDS, dep_map)

        opt_map = CLIBundleKeys.get_option_to_type()
        self.assertIn(CLIBundleKeys.OPTION_SERVICE, opt_map)
        self.assertIn(CLIBundleKeys.OPTION_PARSER, opt_map)
        self.assertIn(CLIBundleKeys.OPTION_GUI, opt_map)

    def test_versions(self) -> None:
        '''Tests registry and factory version retrieval.'''
        self.assertEqual(CLIBundleRegistry.get_version(), '1.0.0')
        self.assertEqual(CLIBundleFactory.get_version(), '1.0.0')

    def test_studio_command_definition(self) -> None:
        '''Tests CLI studio command definition.'''
        cmd = StudioCommandDefinition()
        self.assertEqual(cmd.name, 'studio')
        self.assertIn('Robotic Arm Studio', cmd.help_text)
        options = cmd.options
        option_names = [opt.name for opt in options]
        self.assertIn('--config', option_names)
        self.assertIn('--file', option_names)
        self.assertIn('--port', option_names)
        self.assertIn('--baudrate', option_names)
        self.assertIn('--virtual', option_names)
        self.assertIn('--verbose', option_names)


if __name__ == '__main__':
    main()
