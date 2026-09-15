# -*- coding: UTF-8 -*-

'''
Module
    arm_pose_2d.py
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
    Data transfer object holding 2D calculated joint coordinates and linkage vectors.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class ArmPose2D:
    '''
        Calculated 2D planar positions and orientation angles of robotic linkages.

        It defines:

            :attributes:
                | x0 - Base pedestal center X coordinate.
                | y_sh - Base shoulder pivot Y coordinate.
                | x_el - Elbow joint X coordinate.
                | y_el - Elbow joint Y coordinate.
                | rad_boom - Shoulder boom angle in radians.
                | x_wr - Wrist joint X coordinate.
                | y_wr - Wrist joint Y coordinate.
                | rad_tube - Tube link angle in radians.
                | x_tl - Tool flange X coordinate.
                | y_tl - Tool flange Y coordinate.
                | rad_end - Tool link angle in radians.
                | angles - Raw joint angles tuple [J0..J5] in degrees.
    '''

    x0: float
    y_sh: float
    x_el: float
    y_el: float
    rad_boom: float
    x_wr: float
    y_wr: float
    rad_tube: float
    x_tl: float
    y_tl: float
    rad_end: float
    angles: tuple[float, float, float, float, float, float]
