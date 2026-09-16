# -*- coding: UTF-8 -*-

'''
Module
    virtual_arm_firmware.py
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
    Concrete emulator replicating the RP2040 Pico firmware logic.
'''

from __future__ import annotations

from mecharmory.core.service.firmware.firmware_simulator import FirmwareSimulator
from mecharmory.core.service.firmware.firmware_command_parser import FirmwareCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualArmFirmware:
    '''
        Replicates behavior and ASCII communication protocol of the physical Pico firmware.

        It defines:

            :attributes:
                | _simulator - FirmwareSimulator maintaining angles and motion kinematics.
                | _parser - FirmwareCommandParser handling incoming ASCII commands.
            :methods:
                | __init__ - Initializes simulator and command parser.
                | process_command - Executes command line and yields ASCII responses.
                | update_tick - Advances trajectory interpolation by dt_sec.
                | get_angles - Returns current angles snapshot.
                | is_moving - Returns whether any axis is actively transitioning.
    '''

    _simulator: FirmwareSimulator
    _parser: FirmwareCommandParser

    def __init__(self) -> None:
        '''
            Initializes simulated joints and command parser.
        '''
        self._simulator = FirmwareSimulator()
        self._parser = FirmwareCommandParser()

    def process_command(self, line: str) -> list[str]:
        '''
            Parses and executes an incoming command line.

            :param line: Raw ASCII command string.
            :return: List of simulated output lines.
        '''
        return self._parser.execute(line, self._simulator)

    def update_tick(self, dt_sec: float) -> None:
        '''
            Advances trajectory interpolation by dt_sec.

            :param dt_sec: Elapsed duration in seconds.
        '''
        self._simulator.update_tick(dt_sec)

    def get_angles(self) -> list[float]:
        '''
            Returns current angles snapshot.

            :return: List of 6 current angles in degrees.
        '''
        return self._simulator.get_angles()

    def is_moving(self) -> bool:
        '''
            Returns whether any axis is actively transitioning.

            :return: True if motion is active.
        '''
        return self._simulator.is_moving()
