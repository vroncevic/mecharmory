# -*- coding: UTF-8 -*-

'''
Module
    gui_window_test.py
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
    Unit tests for GuiWindow layout configuration, metrics and lifecycle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.infrastructure.gui.gui_window_style import GuiWindowStyle
from mecharmory.infrastructure.gui.gui_window import GuiWindow

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGuiWindow(TestCase):
    '''
        Test cases for GuiWindow coordinator.

        It defines:

            :methods:
                | test_default_style - Verifies class-level default styling configuration.
                | test_initialization_and_lifecycle - Tests lifecycle state transitions.
                | test_custom_styling - Tests initialization with custom GuiWindowStyle.
    '''

    def test_default_style(self) -> None:
        '''Verifies class-level default styling configuration.'''
        self.assertIsInstance(GuiWindow.DEFAULT_STYLE, GuiWindowStyle)
        self.assertEqual(
            GuiWindow.DEFAULT_STYLE.window_title,
            'Mecharmory - 6-DOF Robotic Arm Studio'
        )
        self.assertEqual(GuiWindow.DEFAULT_STYLE.window_geometry, '1280x920')
        self.assertEqual(GuiWindow.DEFAULT_STYLE.poll_interval_ms, 100)
        self.assertEqual(
            GuiWindow.DEFAULT_STYLE.protocol_delete_window,
            'WM_DELETE_WINDOW'
        )

    def test_initialization_and_lifecycle(self) -> None:
        '''Tests lifecycle state transitions.'''
        arm_model = ArmModel()
        arm_service = MagicMock()
        arm_service.get_model.return_value = arm_model
        serial_service = MagicMock()
        serial_service.is_connected.return_value = False

        window = GuiWindow(arm_service, serial_service)
        try:
            self.assertTrue(window.is_initialized())
            self.assertFalse(window.is_running())
        finally:
            window.stop()
            self.assertFalse(window.is_running())

    def test_custom_styling(self) -> None:
        '''Tests initialization with custom GuiWindowStyle.'''
        arm_model = ArmModel()
        arm_service = MagicMock()
        arm_service.get_model.return_value = arm_model
        serial_service = MagicMock()
        serial_service.is_connected.return_value = False

        custom_style = GuiWindowStyle(window_title='Custom Arms', right_col_width=500)
        window = GuiWindow(arm_service, serial_service, style=custom_style)
        try:
            self.assertTrue(window.is_initialized())
        finally:
            window.stop()


if __name__ == '__main__':
    main()
