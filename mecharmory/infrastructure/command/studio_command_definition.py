# -*- coding: UTF-8 -*-

'''
Module
    studio_command_definition.py
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
    Defines StudioCommandDefinition class for Mecharmory Studio CLI subcommand.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandDefinition:
    '''
        CLI subcommand metadata definition for Mecharmory 6-DOF Robotic Arm Studio.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
        '''
        return 'studio'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
        '''
        return 'Run Mecharmory 6-DOF Robotic Arm Studio graphical interface'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
        '''
        return [
            OptionData(
                name='--config',
                help_text='Path to robot configuration JSON file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--file',
                help_text='Path to motion sequence script file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--port',
                help_text='Serial communication port identifier',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--baudrate',
                help_text='Serial communication baudrate speed',
                action=None,
                default='115200',
                required=False,
                choices=['9600', '19200', '38400', '57600', '115200', '230400', '921600'],
                nargs=None
            ),
            OptionData(
                name='--virtual',
                help_text='Enable or disable virtual simulation mode',
                action=None,
                default='disable',
                required=False,
                choices=['enable', 'disable'],
                nargs=None
            ),
            OptionData(
                name='--verbose',
                help_text='Enable or disable verbose logging output',
                action=None,
                default='disable',
                required=False,
                choices=['enable', 'disable'],
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: String representation.
        '''
        return to_str(self)
