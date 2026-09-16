# -*- coding: UTF-8 -*-

'''
Module
    joint_widget_style_test.py
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
    Unit tests for JointWidgetStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.joint.joint_widget_style import (
    JointWidgetStyle
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointWidgetStyle(TestCase):
    '''
        Test cases for JointWidgetStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default layout and dimension values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default layout and dimension values.'''
        style = JointWidgetStyle()
        self.assertEqual(style.card_pad_x, 10)
        self.assertEqual(style.card_pad_y, 8)
        self.assertEqual(style.card_border_width, 1)
        self.assertEqual(style.slider_resolution, 0.5)
        self.assertEqual(style.step_btn_width, 3)
        self.assertEqual(style.step_btn_pad_y, 1)
        self.assertEqual(style.btn_m5_text, '-5°')
        self.assertEqual(style.btn_m1_text, '-1°')
        self.assertEqual(style.btn_p1_text, '+1°')
        self.assertEqual(style.btn_p5_text, '+5°')
        self.assertEqual(style.step_delta_large, 5.0)
        self.assertEqual(style.step_delta_small, 1.0)
        self.assertEqual(style.entry_width, 5)
        self.assertEqual(style.entry_val_template, '{val:.1f}')
        self.assertEqual(style.btn_set_text, 'Set')
        self.assertEqual(style.btn_set_pad_y, 1)
        self.assertEqual(style.sync_threshold_deg, 0.4)
        self.assertIn('{min_deg:.0f}°', style.range_template)
        self.assertIn('{angle:.1f}°', style.pos_template)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = JointWidgetStyle()
        with self.assertRaises(FrozenInstanceError):
            style.card_pad_x = 20  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = JointWidgetStyle(card_pad_x=15, btn_set_text='Apply')
        self.assertEqual(custom_style.card_pad_x, 15)
        self.assertEqual(custom_style.btn_set_text, 'Apply')


if __name__ == '__main__':
    main()
