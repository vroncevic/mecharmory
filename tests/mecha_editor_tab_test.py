# -*- coding: UTF-8 -*-

'''
Module
    mecha_editor_tab_test.py
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
    Unit tests for MechaEditorTab GUI component.
'''

from __future__ import annotations

from unittest import TestCase, main
from tkinter import Tk

from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.infrastructure.gui.dsl.mecha_editor_tab import MechaEditorTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMechaEditorTab(TestCase):
    '''
        Test cases for MechaEditorTab GUI subcomponents.

        It defines:

            :methods:
                | setUp - Prepares Tkinter root and tab instance.
                | tearDown - Cleans up Tkinter resources.
                | test_initial_state - Tests default demo script loaded.
                | test_load_and_get_script - Tests setting and reading editor text.
                | test_validate_and_compile - Tests GUI validation and compilation triggers.
    '''

    _root: Tk
    _tab: MechaEditorTab
    _sent_commands: list[str]

    def setUp(self) -> None:
        '''Prepares Tkinter root and tab instance.'''
        self._root = Tk()
        self._root.withdraw()
        self._sent_commands = []
        model = ArmModel()
        self._tab = MechaEditorTab(
            self._root,
            on_send_command=self._sent_commands.append,
            model=model
        )

    def tearDown(self) -> None:
        '''Cleans up Tkinter resources.'''
        self._tab.destroy()
        self._root.destroy()

    def test_initial_state(self) -> None:
        '''Tests default demo script loaded.'''
        text = self._tab.get_script()
        self.assertIn('Mecharmo 6-DOF', text)

    def test_load_and_get_script(self) -> None:
        '''Tests setting and reading editor text.'''
        test_script = 'HOME\nWAIT_MS 100\n'
        self._tab.load_script(test_script)
        self.assertEqual(self._tab.get_script(), test_script.strip())

    def test_validate_and_compile(self) -> None:
        '''Tests GUI validation and compilation triggers.'''
        self._tab.load_script('HOME\nMOVE_J BASE 90.0\n')
        self.assertTrue(self._tab.validate_code())
        cmds = self._tab.compile_code()
        self.assertEqual(cmds, ('HOME', 'SET 0 90.00'))


if __name__ == '__main__':
    main()
