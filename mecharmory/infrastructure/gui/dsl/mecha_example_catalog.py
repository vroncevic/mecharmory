# -*- coding: UTF-8 -*-

'''
Module
    mecha_example_catalog.py
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
    Demonstration and example script catalog provider for Mecha DSL.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaExampleCatalog:
    '''
        Demonstration catalog providing standard Mecha DSL operational scripts.

        It defines:

            :attributes:
                | _EXAMPLES - Mapping of demonstration names to script source text.
            :methods:
                | get_example_names - Returns available demonstration names.
                | get_example - Retrieves demonstration script text by name.
    '''

    _EXAMPLES: ClassVar[dict[str, str]] = {
        'Pick & Place Routine': (
            '# ==========================================================\n'
            '# Mecharmo 6-DOF Pick & Place Demonstration (.mecha)\n'
            '# ==========================================================\n'
            'VAR SPEED_SLOW = 30.0\n'
            'VAR SPEED_FAST = 60.0\n'
            'VAR DWELL = 300\n'
            '\n'
            '# Define workspace target postures\n'
            'POINT P_APPROACH = 90.0, 100.0, 80.0, 90.0, 90.0, 90.0\n'
            'POINT P_PICK = 90.0, 120.0, 70.0, 90.0, 90.0, 90.0\n'
            'POINT P_PLACE = 150.0, 110.0, 80.0, 90.0, 90.0, 90.0\n'
            '\n'
            '# 1. Homing & Setup\n'
            'SPEED SPEED_FAST\n'
            'PRESET HOME\n'
            'WAIT_MS DWELL\n'
            '\n'
            '# 2. Move to pick location\n'
            'GRIPPER OPEN\n'
            'MOVE_P P_APPROACH SPEED=SPEED_FAST\n'
            'MOVE_P P_PICK SPEED=SPEED_SLOW\n'
            'WAIT_MS 200\n'
            '\n'
            '# 3. Grip workpiece and lift\n'
            'GRIPPER CLOSE\n'
            'WAIT_MS 400\n'
            'PRESET HIGH_REACH\n'
            'WAIT_MS DWELL\n'
            '\n'
            '# 4. Transfer to place location\n'
            'MOVE_P P_PLACE SPEED=SPEED_SLOW\n'
            'WAIT_MS 200\n'
            'GRIPPER OPEN\n'
            'WAIT_MS 300\n'
            '\n'
            '# 5. Return to home\n'
            'PRESET HOME\n'
        ),
        'Calibration & Homing': (
            '# ==========================================================\n'
            '# Mecharmo Multi-Axis Calibration & Inspection (.mecha)\n'
            '# ==========================================================\n'
            'SPEED 40.0\n'
            'HOME\n'
            'WAIT_MS 500\n'
            '\n'
            '# Individual Joint Verification\n'
            'MOVE_J BASE 120.0\n'
            'WAIT_MS 300\n'
            'MOVE_J BASE 60.0\n'
            'WAIT_MS 300\n'
            'MOVE_J BASE 90.0\n'
            '\n'
            '# Wrist & Tool Roll Test\n'
            'MOVE_J END_PITCH 110.0\n'
            'MOVE_J TOOL_ROLL 135.0\n'
            'WAIT_MS 400\n'
            'HOME\n'
        ),
        'Wave Greeting': (
            '# ==========================================================\n'
            '# Mecharmo Friendly Wave Gesture (.mecha)\n'
            '# ==========================================================\n'
            'SPEED 70.0\n'
            'PRESET HIGH_REACH\n'
            'WAIT_MS 300\n'
            '\n'
            '# Wave wrist back and forth\n'
            'MOVE_J TOOL_ROLL 135.0\n'
            'WAIT_MS 200\n'
            'MOVE_J TOOL_ROLL 45.0\n'
            'WAIT_MS 200\n'
            'MOVE_J TOOL_ROLL 135.0\n'
            'WAIT_MS 200\n'
            'MOVE_J TOOL_ROLL 90.0\n'
            'WAIT_MS 300\n'
            'PRESET HOME\n'
        )
    }

    @classmethod
    def get_example_names(cls) -> list[str]:
        '''
            Returns list of available demonstration script titles.

            :return: List of script name strings.
        '''
        return list(cls._EXAMPLES.keys())

    @classmethod
    def get_example(cls, name: str) -> str:
        '''
            Retrieves script source text for given demonstration name.

            :param name: Example title key.
            :return: Source text or empty string if not found.
        '''
        return cls._EXAMPLES.get(name, '')
