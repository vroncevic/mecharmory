# -*- coding: UTF-8 -*-

'''
Module
    arm_telemetry_parser.py
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
    Parser for incoming firmware telemetry and state feedback strings.
'''

from __future__ import annotations

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.iarm_model import IArmModel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmTelemetryParser:
    '''
        Parses device feedback lines and updates domain joint states.

        It defines:

            :methods:
                | parse - Parses telemetry line and updates model states.
                | _parse_token - Processes single key-value telemetry token.
    '''

    def parse(self, line: str, model: IArmModel) -> bool:
        '''
            Parses status feedback from device and updates model.

            :param line: Raw ASCII line from serial connection.
            :param model: Domain IArmModel aggregate to update.
            :return: True if line was recognized as STATUS telemetry.
        '''
        clean: str = line.strip()
        if not clean.startswith('STATUS'):
            return False

        tokens: list[str] = clean.split()
        for token in tokens[1:]:
            self._parse_token(token, model)

        return True

    def _parse_token(self, token: str, model: IArmModel) -> None:
        '''
            Processes a single status key-value pair.

            :param token: Colon-separated key-value token (e.g., 'J0:90.00').
            :param model: Domain IArmModel aggregate.
        '''
        if ':' not in token:
            return

        key, val_str = token.split(':', 1)
        if key == 'MOVING':
            is_mov: bool = val_str == '1'
            for st in model.get_all_states():
                st.is_moving = is_mov
            return

        if key.startswith('J') and len(key) == 2 and key[1].isdigit():
            jid_int: int = int(key[1])
            if 0 <= jid_int < 6:
                try:
                    model.update_current(JointId(jid_int), float(val_str))
                except ValueError:
                    pass
