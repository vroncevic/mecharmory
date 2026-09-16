# -*- coding: UTF-8 -*-

'''
Module
    joint_id.py
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
    Enumeration of 6-DOF robotic arm joints matching the physical manipulator.
'''

from __future__ import annotations

from enum import IntEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointId(IntEnum):
    '''
        Enumeration of joints for physical 6-DOF robotic manipulator.

        It defines:

            :constants:
                | BASE - Base rotation yaw axis (Joint 0).
                | LIFT_1 - Arm lift servo 1 (Shoulder boom, Joint 1).
                | LIFT_2 - Arm lift servo 2 (Shoulder linkage rod, Joint 2).
                | TUBE_ROLL - Elbow tube axial rotation servo (Joint 3).
                | END_PITCH - Wrist / end bracket tilt servo (Joint 4).
                | TOOL_ROLL - Tool flange / steering wheel rotation (Joint 5).
    '''

    BASE = 0
    LIFT_1 = 1
    LIFT_2 = 2
    TUBE_ROLL = 3
    END_PITCH = 4
    TOOL_ROLL = 5
