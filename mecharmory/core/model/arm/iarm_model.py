# -*- coding: UTF-8 -*-

'''
Module
    iarm_model.py
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
    Abstract protocol interface for the robot arm model aggregate.
'''

from __future__ import annotations

from typing import Iterable, Protocol, runtime_checkable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.kinematics.joint_state import JointState
from mecharmory.core.model.preset.motion_preset import MotionPreset

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArmModel(Protocol):
    '''
        Abstract protocol interface for robotic arm aggregate model.

        It defines:

            :methods:
                | get_config - Retrieves configuration for a joint.
                | get_state - Retrieves current state for a joint.
                | get_all_states - Returns an iterable of all active joint states.
                | get_presets - Returns available postures.
                | clamp_angle - Constrains angle value within joint boundaries.
                | update_target - Sets desired angle for a joint after validation.
                | update_current - Updates actual reported angle.
    '''

    def get_config(self, joint_id: JointId) -> JointConfig:
        '''
            Retrieves configuration for a joint.

            :param joint_id: Target joint ID.
            :return: JointConfig object.
        '''

    def get_state(self, joint_id: JointId) -> JointState:
        '''
            Retrieves current state for a joint.

            :param joint_id: Target joint ID.
            :return: JointState object.
        '''

    def get_all_states(self) -> Iterable[JointState]:
        '''
            Returns an iterable of all active joint states.

            :return: Iterable of JointState.
        '''

    def get_presets(self) -> tuple[MotionPreset, ...]:
        '''
            Returns available postures.

            :return: Tuple of MotionPreset.
        '''

    def clamp_angle(self, joint_id: JointId, angle: float) -> float:
        '''
            Constrains angle value within joint boundaries.

            :param joint_id: Target joint ID.
            :param angle: Commanded angle value.
            :return: Clamped angle value in degrees.
        '''

    def update_target(self, joint_id: JointId, angle: float) -> float:
        '''
            Sets desired angle for a joint after validation.

            :param joint_id: Target joint ID.
            :param angle: Desired angle.
            :return: Clamped angle applied to target.
        '''

    def update_current(self, joint_id: JointId, angle: float) -> None:
        '''
            Updates actual reported angle.

            :param joint_id: Target joint ID.
            :param angle: Reported angle.
        '''
