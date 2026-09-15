# -*- coding: UTF-8 -*-

'''
Module
    iarm_controller_service.py
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
    Abstract protocol interface for robotic arm coordination service.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.model.arm.iarm_model import IArmModel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArmControllerService(Protocol):
    '''
        Defines operational contract for arm control logic.

        It defines:

            :methods:
                | is_initialized - Checks if arm controller service is initialized.
                | get_model - Returns the active arm model interface.
                | move_joint - Dispatches a target angle for a single joint.
                | move_all - Dispatches angles for all 6 joints simultaneously.
                | set_speed - Updates velocity limit for a joint.
                | stop - Commands emergency stop on all axes.
                | home - Moves all axes smoothly to home position.
                | apply_preset - Executes target angles defined in a preset.
                | query_status - Queries current status from device.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if arm controller service is initialized.

            :return: True if initialized, False otherwise.
        '''

    def get_model(self) -> IArmModel:
        '''
            Returns the active arm model interface.

            :return: IArmModel instance.
        '''

    def move_joint(self, joint_id: JointId, target_deg: float) -> bool:
        '''
            Dispatches a target angle for a single joint.

            :param joint_id: Target joint ID.
            :param target_deg: Commanded angle in degrees.
            :return: True if successfully sent.
        '''

    def move_all(self, angles: tuple[float, ...]) -> bool:
        '''
            Dispatches angles for all 6 joints simultaneously.

            :param angles: Tuple of 6 angles in degrees.
            :return: True if successfully sent.
        '''

    def set_speed(self, joint_id: JointId, speed_deg_s: float) -> bool:
        '''
            Updates velocity limit for a joint.

            :param joint_id: Target joint ID.
            :param speed_deg_s: Speed in deg/s.
            :return: True if successfully sent.
        '''

    def stop(self) -> bool:
        '''
            Commands emergency stop on all axes.

            :return: True if successfully sent.
        '''

    def home(self) -> bool:
        '''
            Moves all axes smoothly to home position.

            :return: True if successfully sent.
        '''

    def apply_preset(self, preset: MotionPreset) -> bool:
        '''
            Executes target angles defined in a preset.

            :param preset: MotionPreset value object.
            :return: True if successfully sent.
        '''

    def query_status(self) -> bool:
        '''
            Queries current status telemetry from device.

            :return: True if query sent.
        '''
