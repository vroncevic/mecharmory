# -*- coding: UTF-8 -*-

'''
Module
    ivirtual_arm_firmware.py
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
    Abstract protocol interface for simulated virtual arm firmware.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IVirtualArmFirmware(Protocol):
    '''
        Defines behavior of firmware emulator for Mecharmo.

        It defines:

            :methods:
                | process_command - Executes command line and yields ASCII responses.
                | update_tick - Advances trajectory interpolation by dt_sec.
                | get_angles - Returns current angles snapshot.
                | is_moving - Returns whether any axis is actively transitioning.
    '''

    def process_command(self, line: str) -> list[str]:
        '''
            Executes command line and yields ASCII responses.

            :param line: Raw ASCII command string.
            :return: List of simulated output lines.
        '''

    def update_tick(self, dt_sec: float) -> None:
        '''
            Advances trajectory interpolation by dt_sec.

            :param dt_sec: Elapsed duration in seconds.
        '''

    def get_angles(self) -> list[float]:
        '''
            Returns current angles snapshot.

            :return: List of 6 current angles in degrees.
        '''

    def is_moving(self) -> bool:
        '''
            Returns whether any axis is actively transitioning.

            :return: True if motion is active.
        '''
