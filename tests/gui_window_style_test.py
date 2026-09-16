# -*- coding: UTF-8 -*-

'''
Module
    gui_window_style_test.py
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
    Unit tests for GuiWindowStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.gui_window_style import GuiWindowStyle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGuiWindowStyle(TestCase):
    '''
        Test cases for GuiWindowStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default window metrics and styling values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default window metrics and styling values.'''
        style = GuiWindowStyle()
        self.assertEqual(style.window_title, 'Mecharmory - 6-DOF Robotic Arm Studio')
        self.assertEqual(style.window_geometry, '1280x920')
        self.assertEqual(style.poll_interval_ms, 100)
        self.assertEqual(style.protocol_delete_window, 'WM_DELETE_WINDOW')
        self.assertEqual(style.body_pad_x, 10)
        self.assertEqual(style.body_pad_y, 8)
        self.assertEqual(style.upper_row_spacing_y, (0, 8))
        self.assertEqual(style.left_col_spacing_x, (0, 8))
        self.assertEqual(style.control_panel_spacing_y, (0, 8))
        self.assertEqual(style.right_col_width, 480)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = GuiWindowStyle()
        with self.assertRaises(FrozenInstanceError):
            style.window_title = 'Custom Title'  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = GuiWindowStyle(
            window_title='Custom Studio',
            window_geometry='1920x1080',
            poll_interval_ms=20,
            right_col_width=500
        )
        self.assertEqual(custom_style.window_title, 'Custom Studio')
        self.assertEqual(custom_style.window_geometry, '1920x1080')
        self.assertEqual(custom_style.poll_interval_ms, 20)
        self.assertEqual(custom_style.right_col_width, 500)


if __name__ == '__main__':
    main()
