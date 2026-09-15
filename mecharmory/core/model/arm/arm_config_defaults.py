# -*- coding: UTF-8 -*-

'''
Module
    arm_config_defaults.py
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
    Default calibration configurations factory for robotic arm joints.
'''

from __future__ import annotations

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmConfigDefaults:
    '''
        Factory providing factory default joint calibration configurations.

        It defines:

            :methods:
                | get_default_configs - Generates standard calibration mapping.
    '''

    @classmethod
    def get_default_configs(cls) -> dict[JointId, JointConfig]:
        '''
            Generates standard calibration mapping for physical 6-DOF assembly.

            :return: Mapping of JointId to JointConfig.
            :exceptions: None.
        '''
        return {
            JointId.BASE: JointConfig(
                joint_id=JointId.BASE,
                name='J0: Base (Yaw)',
                channel=0,
                min_deg=0.0,
                max_deg=180.0,
                home_deg=90.0,
                default_speed_deg_s=60.0,
                min_pulse_us=500,
                max_pulse_us=2500
            ),
            JointId.LIFT_1: JointConfig(
                joint_id=JointId.LIFT_1,
                name='J1: Shoulder Left (Pitch)',
                channel=1,
                min_deg=15.0,
                max_deg=165.0,
                home_deg=90.0,
                default_speed_deg_s=40.0,
                min_pulse_us=600,
                max_pulse_us=2400
            ),
            JointId.LIFT_2: JointConfig(
                joint_id=JointId.LIFT_2,
                name='J2: Shoulder Right (Pitch)',
                channel=2,
                min_deg=15.0,
                max_deg=165.0,
                home_deg=90.0,
                default_speed_deg_s=40.0,
                min_pulse_us=600,
                max_pulse_us=2400
            ),
            JointId.TUBE_ROLL: JointConfig(
                joint_id=JointId.TUBE_ROLL,
                name='J3: Elbow (Roll)',
                channel=3,
                min_deg=0.0,
                max_deg=180.0,
                home_deg=90.0,
                default_speed_deg_s=70.0,
                min_pulse_us=500,
                max_pulse_us=2500
            ),
            JointId.END_PITCH: JointConfig(
                joint_id=JointId.END_PITCH,
                name='J4: Wrist (Pitch)',
                channel=4,
                min_deg=15.0,
                max_deg=165.0,
                home_deg=90.0,
                default_speed_deg_s=80.0,
                min_pulse_us=500,
                max_pulse_us=2500
            ),
            JointId.TOOL_ROLL: JointConfig(
                joint_id=JointId.TOOL_ROLL,
                name='J5: Tool (Roll)',
                channel=5,
                min_deg=0.0,
                max_deg=180.0,
                home_deg=90.0,
                default_speed_deg_s=90.0,
                min_pulse_us=500,
                max_pulse_us=2500
            ),
        }
