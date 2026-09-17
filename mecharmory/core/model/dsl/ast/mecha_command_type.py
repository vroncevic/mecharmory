# -*- coding: UTF-8 -*-

'''
Module
    mecha_command_type.py
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
    Defines MechaCommandType enumeration representing all supported Mecha DSL commands.
'''

from __future__ import annotations

from enum import Enum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class MechaCommandType(Enum):
    '''
        Enumeration of supported Mecha Domain-Specific Language (DSL) command types.

        It defines:

            :constants:
                | VAR - Scalar numeric variable declaration.
                | POINT - 6-DOF joint coordinates posture definition.
                | MOVE_P - Synchronized move of all 6 axes to target posture.
                | MOVE_J - Move single joint to target angle.
                | MOVE_REL - Relative offset rotation of single joint.
                | PRESET - Predefined posture preset movement.
                | SPEED - Global trajectory speed setting in deg/s.
                | SPEED_JOINT - Per-joint actuator speed setting.
                | OVERRIDE - Global feedrate override percentage.
                | GRIPPER - End-effector gripper actuation (OPEN, CLOSE, ANGLE).
                | TOOL_ROLL - End-effector tool flange rotation.
                | WAIT_MS - Execution dwell delay in milliseconds.
                | SYNC - Wait for motion queue execution to complete.
                | HOME - Multi-axis calibration and return to home posture.
                | STOP - Immediate motion halt across all actuators.
                | STATUS - Manipulator telemetry status inquiry.
                | PING - Controller heartbeat verification.
    '''

    VAR = 'VAR'
    POINT = 'POINT'
    MOVE_P = 'MOVE_P'
    MOVE_J = 'MOVE_J'
    MOVE_REL = 'MOVE_REL'
    PRESET = 'PRESET'
    SPEED = 'SPEED'
    SPEED_JOINT = 'SPEED_JOINT'
    OVERRIDE = 'OVERRIDE'
    GRIPPER = 'GRIPPER'
    TOOL_ROLL = 'TOOL_ROLL'
    WAIT_MS = 'WAIT_MS'
    SYNC = 'SYNC'
    HOME = 'HOME'
    STOP = 'STOP'
    STATUS = 'STATUS'
    PING = 'PING'
