# -*- coding: UTF-8 -*-

'''
Module
    arm_command_formatter.py
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
    ASCII command protocol formatter for robotic arm motion operations.
'''

from __future__ import annotations

from mecharmory.core.model.kinematics.joint_id import JointId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmCommandFormatter:
    '''
        Builds formatted ASCII command lines matching the firmware specification.

        It defines:

            :methods:
                | format_set - Generates SET command line.
                | format_setp - Generates SETP command line.
                | format_speed - Generates SPEED command line.
                | format_stop - Generates STOP command line.
                | format_home - Generates HOME command line.
                | format_status - Generates STATUS query line.
    '''

    @classmethod
    def format_set(cls, joint_id: JointId, angle: float) -> str:
        '''
            Generates SET command line.

            :param joint_id: Target joint ID.
            :param angle: Commanded angle value.
            :return: Formatted ASCII command string.
        '''
        return f'SET {int(joint_id)} {angle:.2f}'

    @classmethod
    def format_setp(cls, angles: list[float]) -> str:
        '''
            Generates SETP multi-axis command line.

            :param angles: List of 6 target angles in degrees.
            :return: Formatted ASCII command string.
        '''
        return (
            f'SETP {angles[0]:.2f} {angles[1]:.2f} '
            f'{angles[2]:.2f} {angles[3]:.2f} '
            f'{angles[4]:.2f} {angles[5]:.2f}'
        )

    @classmethod
    def format_speed(cls, joint_id: JointId, speed_deg_s: float) -> str:
        '''
            Generates SPEED command line.

            :param joint_id: Target joint ID.
            :param speed_deg_s: Commanded speed in deg/s.
            :return: Formatted ASCII command string.
        '''
        return f'SPEED {int(joint_id)} {speed_deg_s:.2f}'

    @classmethod
    def format_stop(cls) -> str:
        '''
            Generates STOP command line.

            :return: Formatted ASCII command string.
        '''
        return 'STOP'

    @classmethod
    def format_home(cls) -> str:
        '''
            Generates HOME command line.

            :return: Formatted ASCII command string.
        '''
        return 'HOME'

    @classmethod
    def format_status(cls) -> str:
        '''
            Generates STATUS query command line.

            :return: Formatted ASCII command string.
        '''
        return 'STATUS'
