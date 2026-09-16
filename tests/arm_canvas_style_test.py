# -*- coding: UTF-8 -*-

'''
Module
    arm_canvas_style_test.py
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
    Unit tests for ArmCanvasStyle data model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.canvas.arm_canvas_style import ArmCanvasStyle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmCanvasStyle(TestCase):
    '''
        Test cases for ArmCanvasStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default visual and geometry values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default visual and geometry values.'''
        style = ArmCanvasStyle()
        self.assertEqual(style.ground_text, 'GROUND')
        self.assertEqual(style.ground_line_width, 2)
        self.assertEqual(style.pedestal_half_width, 26.0)
        self.assertEqual(style.turntable_radius_x, 18.0)
        self.assertEqual(style.turntable_radius_y, 6.0)
        self.assertEqual(style.rod_offset, 9.0)
        self.assertEqual(style.boom_line_width, 7)
        self.assertEqual(style.shoulder_joint_radius, 6.0)
        self.assertEqual(style.elbow_joint_radius, 7.0)
        self.assertEqual(style.wrist_joint_radius, 5.0)
        self.assertEqual(style.tool_flange_radius, 12.0)
        self.assertEqual(style.hud_anchor, 'ne')
        self.assertIn('{0:.0f}', style.hud_template)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = ArmCanvasStyle()
        with self.assertRaises(FrozenInstanceError):
            style.ground_text = 'FLOOR'  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = ArmCanvasStyle(ground_text='BASE', pedestal_half_width=30.0)
        self.assertEqual(custom_style.ground_text, 'BASE')
        self.assertEqual(custom_style.pedestal_half_width, 30.0)


if __name__ == '__main__':
    main()
