# -*- coding: UTF-8 -*-

'''
Module
    joint_state.py
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
    Entity representing dynamic state of a robot joint.
'''

from __future__ import annotations

from dataclasses import dataclass

from mecharmory.core.model.kinematics.joint_id import JointId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class JointState:
    '''
        Represents dynamic runtime state of a single robotic joint.

        It defines:

            :attributes:
                | joint_id - Identifier of the joint.
                | current_angle - Actual current estimated or reported angle.
                | target_angle - Commanded target angle in degrees.
                | speed_deg_s - Current speed setting in degrees per second.
                | is_moving - Boolean flag indicating active interpolation.
    '''

    joint_id: JointId
    current_angle: float
    target_angle: float
    speed_deg_s: float
    is_moving: bool = False
