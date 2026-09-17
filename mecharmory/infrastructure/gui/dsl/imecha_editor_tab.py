# -*- coding: UTF-8 -*-

'''
Module
    imecha_editor_tab.py
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
    Defines abstract protocol IMechaEditorTab for the Mecha DSL editor GUI container.
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
class IMechaEditorTab(Protocol):
    '''
        Abstract protocol for the Mecha DSL Editor tab component.

        It defines:

            :methods:
                | load_script - Inserts script text into code editor buffer.
                | get_script - Returns active editor buffer string.
                | validate_code - Runs linter and updates diagnostic console.
                | compile_code - Translates active code into firmware commands.
                | run_script - Starts asynchronous execution on robot serial bridge.
                | stop_script - Aborts active execution.
    '''

    def load_script(self, text: str) -> None:
        '''
            Loads script content into editor.

            :param text: Source code string.
        '''

    def get_script(self) -> str:
        '''
            Retrieves current script text from editor buffer.

            :return: String content.
        '''

    def validate_code(self) -> bool:
        '''
            Validates active script and displays diagnostics.

            :return: True if valid without errors, False otherwise.
        '''

    def compile_code(self) -> tuple[str, ...]:
        '''
            Compiles active script into firmware command lines.

            :return: Tuple of compiled commands.
        '''

    def run_script(self) -> None:
        '''Executes compiled commands on the robot.'''

    def stop_script(self) -> None:
        '''Stops running script execution.'''
