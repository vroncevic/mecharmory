# -*- coding: UTF-8 -*-

'''
Module
    motion_preset_test.py
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
    Unit tests for MotionPreset value object.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.preset.motion_preset import MotionPreset

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionPreset(TestCase):
    '''
        Test cases for MotionPreset value object.

        It defines:

            :methods:
                | test_preset_creation - Tests initialization of a motion preset.
                | test_preset_immutability - Tests frozen state of a motion preset.
    '''

    def test_preset_creation(self) -> None:
        '''Tests initialization of a motion preset.'''
        angles = (90.0, 90.0, 90.0, 90.0, 90.0, 90.0)
        preset = MotionPreset(
            name='Home Position',
            description='Central neutral posture',
            angles=angles
        )
        self.assertEqual(preset.name, 'Home Position')
        self.assertEqual(preset.description, 'Central neutral posture')
        self.assertEqual(preset.angles, angles)
        self.assertEqual(len(preset.angles), 6)

    def test_preset_immutability(self) -> None:
        '''Tests frozen state of a motion preset.'''
        preset = MotionPreset(
            name='Park',
            description='Park position',
            angles=(90.0, 35.0, 145.0, 90.0, 90.0, 90.0)
        )
        with self.assertRaises(AttributeError):
            preset.name = 'New Name'  # type: ignore


if __name__ == '__main__':
    main()
