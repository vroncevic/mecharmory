# -*- coding: UTF-8 -*-

'''
Module
    arm_panel_style_test.py
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
    Unit tests for ArmPanelStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.arm.arm_panel_style import ArmPanelStyle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmPanelStyle(TestCase):
    '''
        Test cases for ArmPanelStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default layout and label values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default layout and label values.'''
        style = ArmPanelStyle()
        self.assertEqual(style.panel_pad_x, 12)
        self.assertEqual(style.panel_pad_y, 10)
        self.assertEqual(style.header_pad_bottom, 10)
        self.assertEqual(style.title_text, 'JOINT CONTROLS')
        self.assertEqual(style.title_font_weight, 'bold')
        self.assertEqual(style.btn_font_weight, 'bold')
        self.assertEqual(style.btn_stop_text, 'EMERGENCY STOP')
        self.assertEqual(style.btn_home_text, 'Home All')
        self.assertEqual(style.btn_query_text, 'Query Status')
        self.assertEqual(style.btn_stop_fg, '#ffffff')
        self.assertEqual(style.joint_widget_pad_y, 3)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = ArmPanelStyle()
        with self.assertRaises(FrozenInstanceError):
            style.title_text = 'NEW TITLE'  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = ArmPanelStyle(title_text='CUSTOM ARM', panel_pad_x=20)
        self.assertEqual(custom_style.title_text, 'CUSTOM ARM')
        self.assertEqual(custom_style.panel_pad_x, 20)


if __name__ == '__main__':
    main()
