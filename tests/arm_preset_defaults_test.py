# -*- coding: UTF-8 -*-

'''
Module
    arm_preset_defaults_test.py
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
    Unit tests for ArmPresetDefaults factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.arm.arm_preset_defaults import ArmPresetDefaults
from mecharmory.core.model.preset.motion_preset import MotionPreset

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmPresetDefaults(TestCase):
    '''
        Test cases for ArmPresetDefaults factory.

        It defines:

            :methods:
                | test_get_individual_presets - Tests getters for individual posture presets.
                | test_get_default_presets - Tests full collection of default presets.
                | test_get_preset_by_name - Tests searching preset by name.
    '''

    def test_get_individual_presets(self) -> None:
        '''Tests getters for individual posture presets.'''
        home: MotionPreset = ArmPresetDefaults.get_home_preset()
        self.assertEqual(home.name, 'Home Position')
        self.assertEqual(home.angles, (90.0, 90.0, 90.0, 90.0, 90.0, 90.0))

        parked: MotionPreset = ArmPresetDefaults.get_parked_preset()
        self.assertEqual(parked.name, 'Parked (Folded)')
        self.assertEqual(parked.angles, (90.0, 35.0, 145.0, 90.0, 90.0, 90.0))

        forward: MotionPreset = ArmPresetDefaults.get_forward_reach_preset()
        self.assertEqual(forward.name, 'Forward Reach')
        self.assertEqual(forward.angles, (90.0, 120.0, 70.0, 90.0, 90.0, 90.0))

        high: MotionPreset = ArmPresetDefaults.get_high_reach_preset()
        self.assertEqual(high.name, 'High Reach')
        self.assertEqual(high.angles, (90.0, 135.0, 120.0, 90.0, 90.0, 90.0))

    def test_get_default_presets(self) -> None:
        '''Tests full collection of default presets.'''
        presets: tuple[MotionPreset, ...] = ArmPresetDefaults.get_default_presets()
        self.assertEqual(len(presets), 4)
        self.assertEqual(presets[0], ArmPresetDefaults.get_home_preset())
        self.assertEqual(presets[1], ArmPresetDefaults.get_parked_preset())
        self.assertEqual(presets[2], ArmPresetDefaults.get_forward_reach_preset())
        self.assertEqual(presets[3], ArmPresetDefaults.get_high_reach_preset())

    def test_get_preset_by_name(self) -> None:
        '''Tests searching preset by name.'''
        found = ArmPresetDefaults.get_preset_by_name('Home Position')
        self.assertIsNotNone(found)
        if found is not None:
            self.assertEqual(found.name, 'Home Position')

        not_found = ArmPresetDefaults.get_preset_by_name('Non Existent Position')
        self.assertIsNone(not_found)


if __name__ == '__main__':
    main()
