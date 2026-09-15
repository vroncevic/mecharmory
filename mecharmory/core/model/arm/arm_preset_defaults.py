# -*- coding: UTF-8 -*-

'''
Module
    arm_preset_defaults.py
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
    Default posture presets factory for robotic arm manipulator.
'''

from __future__ import annotations

from mecharmory.core.model.preset.motion_preset import MotionPreset

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmPresetDefaults:
    '''
        Factory providing default motion postures for the robot arm.

        It defines:

            :methods:
                | get_home_preset - Generates central neutral posture preset.
                | get_parked_preset - Generates compact folded arm posture preset.
                | get_forward_reach_preset - Generates extended posture preset.
                | get_high_reach_preset - Generates elevated posture preset.
                | get_preset_by_name - Retrieves preset instance by name.
                | get_default_presets - Generates standard predefined postures.
    '''

    @classmethod
    def get_home_preset(cls) -> MotionPreset:
        '''
            Generates central neutral posture preset.

            :return: MotionPreset instance for home posture.
            :exceptions: None.
        '''
        return MotionPreset(
            name='Home Position',
            description='Central neutral posture',
            angles=(90.0, 90.0, 90.0, 90.0, 90.0, 90.0)
        )

    @classmethod
    def get_parked_preset(cls) -> MotionPreset:
        '''
            Generates compact folded arm posture preset.

            :return: MotionPreset instance for parked posture.
            :exceptions: None.
        '''
        return MotionPreset(
            name='Parked (Folded)',
            description='Compact folded arm posture',
            angles=(90.0, 35.0, 145.0, 90.0, 90.0, 90.0)
        )

    @classmethod
    def get_forward_reach_preset(cls) -> MotionPreset:
        '''
            Generates extended forward posture preset for workspace operation.

            :return: MotionPreset instance for forward reach posture.
            :exceptions: None.
        '''
        return MotionPreset(
            name='Forward Reach',
            description='Arm extended forward for workspace operation',
            angles=(90.0, 120.0, 70.0, 90.0, 90.0, 90.0)
        )

    @classmethod
    def get_high_reach_preset(cls) -> MotionPreset:
        '''
            Generates elevated arm posture preset for high reach.

            :return: MotionPreset instance for high reach posture.
            :exceptions: None.
        '''
        return MotionPreset(
            name='High Reach',
            description='Elevated arm posture for high reach',
            angles=(90.0, 135.0, 120.0, 90.0, 90.0, 90.0)
        )

    @classmethod
    def get_preset_by_name(cls, name: str) -> MotionPreset | None:
        '''
            Finds default preset by its exact name.

            :param name: Name of the preset to find.
            :return: Matching MotionPreset instance or None if not found.
            :exceptions: None.
        '''
        for preset in cls.get_default_presets():
            if preset.name == name:
                return preset
        return None

    @classmethod
    def get_default_presets(cls) -> tuple[MotionPreset, ...]:
        '''
            Generates standard predefined postures for the robot arm.

            :return: Tuple of MotionPreset instances.
            :exceptions: None.
        '''
        return (
            cls.get_home_preset(),
            cls.get_parked_preset(),
            cls.get_forward_reach_preset(),
            cls.get_high_reach_preset(),
        )
