# -*- coding: UTF-8 -*-

'''
Module
    firmware_command_parser.py
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
    ASCII command parser and response generator for virtual firmware emulator.
'''

from __future__ import annotations

from mecharmory.core.service.firmware.firmware_simulator import FirmwareSimulator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FirmwareCommandParser:
    '''
        Parses ASCII commands and delegates state execution to FirmwareSimulator.

        It defines:

            :methods:
                | execute - Parses command string and returns output responses.
                | _format_status - Formats current simulated status line.
                | _cmd_get - Handles GET joint inquiry command.
                | _cmd_set - Handles SET single joint angle command.
                | _cmd_setp - Handles SETP multi-joint posture command.
                | _cmd_speed - Handles SPEED velocity limit command.
    '''

    def execute(self, line: str, simulator: FirmwareSimulator) -> list[str]:
        '''
            Parses and executes an incoming ASCII command line.

            :param line: Raw ASCII command string.
            :param simulator: FirmwareSimulator instance to operate upon.
            :return: List of simulated output response lines.
        '''
        clean: str = line.strip()
        if not clean:
            return []

        tokens: list[str] = clean.split()
        verb: str = tokens[0].upper()

        match verb:
            case 'PING':
                return ['PONG']
            case 'HOME':
                simulator.home()
                return ['ACK: HOME']
            case 'STOP':
                simulator.stop()
                return ['ACK: STOP']
            case 'STATUS':
                return [self._format_status(simulator)]
            case 'GET':
                return [self._cmd_get(tokens, simulator)]
            case 'SET':
                return [self._cmd_set(tokens, simulator)]
            case 'SETP':
                return [self._cmd_setp(tokens, simulator)]
            case 'SPEED':
                return [self._cmd_speed(tokens, simulator)]
            case _:
                return ['ERR: Unknown command']

    def _format_status(self, simulator: FirmwareSimulator) -> str:
        '''
            Formats status response line from simulator angles.

            :param simulator: Active FirmwareSimulator.
            :return: Formatted STATUS ASCII string.
        '''
        angles: list[float] = simulator.get_angles()
        moving_flag: int = 1 if simulator.is_moving() else 0
        return (
            f'STATUS J0:{angles[0]:.2f} J1:{angles[1]:.2f} '
            f'J2:{angles[2]:.2f} J3:{angles[3]:.2f} '
            f'J4:{angles[4]:.2f} J5:{angles[5]:.2f} '
            f'MOVING:{moving_flag}'
        )

    def _cmd_get(self, tokens: list[str], simulator: FirmwareSimulator) -> str:
        '''
            Processes GET command.

            :param tokens: Command tokens.
            :param simulator: Active FirmwareSimulator.
            :return: Response string.
        '''
        if len(tokens) < 2:
            return 'ERR: Invalid joint parameter'
        try:
            jid: int = int(tokens[1])
            angle: float | None = simulator.get_angle(jid)
            if angle is not None:
                return f'JOINT {jid} CURRENT {angle:.2f}'
            return f'ERR: Unknown joint ID: {jid}'
        except ValueError:
            return 'ERR: Invalid joint index'

    def _cmd_set(self, tokens: list[str], simulator: FirmwareSimulator) -> str:
        '''
            Processes SET command.

            :param tokens: Command tokens.
            :param simulator: Active FirmwareSimulator.
            :return: Response string.
        '''
        if len(tokens) < 3:
            return 'ERR: Missing parameters for SET'
        try:
            jid: int = int(tokens[1])
            deg: float = float(tokens[2])
            if simulator.get_angle(jid) is None:
                return f'ERR: Unknown joint ID: {jid}'
            if simulator.set_angle(jid, deg):
                return f'ACK: SET {jid} {deg:.2f}'
            return f'ERR: Angle out of limits for joint {jid}'
        except ValueError:
            return 'ERR: Invalid number format'

    def _cmd_setp(self, tokens: list[str], simulator: FirmwareSimulator) -> str:
        '''
            Processes SETP command.

            :param tokens: Command tokens.
            :param simulator: Active FirmwareSimulator.
            :return: Response string.
        '''
        if len(tokens) < 7:
            return 'ERR: SETP requires 6 angle parameters'
        try:
            angles: list[float] = [float(t) for t in tokens[1:7]]
            if simulator.set_all_angles(angles):
                return 'ACK: SETP'
            return 'ERR: One or more angles exceed physical limits'
        except ValueError:
            return 'ERR: Invalid angle values'

    def _cmd_speed(self, tokens: list[str], simulator: FirmwareSimulator) -> str:
        '''
            Processes SPEED command.

            :param tokens: Command tokens.
            :param simulator: Active FirmwareSimulator.
            :return: Response string.
        '''
        if len(tokens) < 3:
            return 'ERR: Missing parameters for SPEED'
        try:
            jid: int = int(tokens[1])
            spd: float = float(tokens[2])
            if simulator.get_angle(jid) is None:
                return f'ERR: Unknown joint ID: {jid}'
            if simulator.set_speed(jid, spd):
                return f'ACK: SPEED {jid} {spd:.2f}'
            return f'ERR: Invalid speed: {spd}'
        except ValueError:
            return 'ERR: Invalid speed parameter'
