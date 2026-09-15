# -*- coding: UTF-8 -*-

'''
Module
    options.py
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
    Mecharmory bundle options TypedDict definition.
'''

from __future__ import annotations

from typing import TypedDict

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryBundleOptions(TypedDict, total=False):
    '''
        Mecharmory bundle options specification.

        It defines:

            :attributes:
                | info_file - Path to the ats info configuration file.
                | config_file - Path to custom robot kinematics JSON config file.
                | scheme_file - Path to config schema validation file.
                | len1 - Base-to-elbow link length in mm.
                | len2 - Elbow-to-wrist link length in mm.
                | len3 - Wrist-to-tool link length in mm.
                | min_speed - Minimum speed limit in deg/s.
                | max_speed - Maximum speed limit in deg/s.
                | default_speed - Default speed in deg/s.
    '''

    info_file: str
    config_file: str
    scheme_file: str
    len1: float
    len2: float
    len3: float
    min_speed: float
    max_speed: float
    default_speed: float
