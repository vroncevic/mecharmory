# -*- coding: UTF-8 -*-

'''
Module
    arm_kinematics_2d.py
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
    2D forward planar kinematics calculator for robotic arm links.
'''

from __future__ import annotations

from math import cos, sin, radians

from mecharmory.infrastructure.gui.canvas.arm_pose_2d import ArmPose2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmKinematics2D:
    '''
        Computes 2D link endpoints and angles for robot arm posture visualization.

        It defines:

            :methods:
                | compute_pose - Calculates 2D planar linkage coordinates.
    '''

    @classmethod
    def compute_pose(
        cls,
        angles: list[float],
        ground_y: float = 265.0
    ) -> ArmPose2D:
        '''
            Calculates 2D planar coordinates for all robot arm segments.

            :param angles: List of 6 joint angles in degrees [J0..J5].
            :param ground_y: Base ground level Y coordinate.
            :return: Computed ArmPose2D object.
            :exceptions: None.
        '''
        x0: float = 75.0
        y_sh: float = ground_y - 45.0

        j1: float = angles[1]
        j2: float = angles[2]
        j4: float = angles[4]

        len1: float = 72.0
        rad_boom: float = radians(180.0 - j1)
        x_el: float = x0 + len1 * cos(rad_boom)
        y_el: float = y_sh - len1 * sin(rad_boom)

        len2: float = 90.0
        rad_tube: float = rad_boom + radians(90.0 - j2)
        x_wr: float = x_el + len2 * cos(rad_tube)
        y_wr: float = y_el - len2 * sin(rad_tube)

        len3: float = 32.0
        rad_end: float = rad_tube + radians(90.0 - j4)
        x_tl: float = x_wr + len3 * cos(rad_end)
        y_tl: float = y_wr - len3 * sin(rad_end)

        angles_tuple: tuple[float, float, float, float, float, float] = (
            angles[0], angles[1], angles[2], angles[3], angles[4], angles[5]
        )

        return ArmPose2D(
            x0=x0,
            y_sh=y_sh,
            x_el=x_el,
            y_el=y_el,
            rad_boom=rad_boom,
            x_wr=x_wr,
            y_wr=y_wr,
            rad_tube=rad_tube,
            x_tl=x_tl,
            y_tl=y_tl,
            rad_end=rad_end,
            angles=angles_tuple
        )
