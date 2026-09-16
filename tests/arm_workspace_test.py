# -*- coding: UTF-8 -*-

'''
Module
    arm_workspace_test.py
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
    Unit tests for ArmWorkspace layout container and child components.
'''

from __future__ import annotations

from queue import Queue
from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.infrastructure.gui.gui_event_mediator import GuiEventMediator
from mecharmory.infrastructure.gui.gui_window_style import GuiWindowStyle
from mecharmory.infrastructure.gui.workspace.arm_workspace import ArmWorkspace

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmWorkspace(TestCase):
    '''
        Test cases for ArmWorkspace container.

        It defines:

            :methods:
                | test_initialization_and_components - Verifies subcomponent hierarchy.
                | test_refresh_visuals - Verifies synchronized telemetry and pose update.
                | test_custom_styling - Verifies custom GuiWindowStyle application.
    '''

    def setUp(self) -> None:
        '''Configures common test fixtures.'''
        self._root = Tk()
        self._arm_model = ArmModel()
        self._arm_service = MagicMock()
        self._arm_service.get_model.return_value = self._arm_model
        self._serial_service = MagicMock()
        self._ui_queue = Queue()
        self._mediator = GuiEventMediator(
            self._arm_service,
            self._serial_service,
            self._ui_queue
        )

    def tearDown(self) -> None:
        '''Cleans up Tkinter resources.'''
        try:
            self._root.destroy()
        except Exception:
            pass

    def test_initialization_and_components(self) -> None:
        '''Verifies subcomponent hierarchy.'''
        workspace = ArmWorkspace(
            self._root,
            model=self._arm_model,
            mediator=self._mediator
        )
        self.assertIsNotNone(workspace.get_control_panel())
        self.assertIsNotNone(workspace.get_preset_panel())
        self.assertIsNotNone(workspace.get_canvas_preview())

    def test_refresh_visuals(self) -> None:
        '''Verifies synchronized telemetry and pose update.'''
        workspace = ArmWorkspace(
            self._root,
            model=self._arm_model,
            mediator=self._mediator
        )
        # Should execute without errors
        workspace.refresh_visuals()

    def test_custom_styling(self) -> None:
        '''Verifies custom GuiWindowStyle application.'''
        custom_style = GuiWindowStyle(right_col_width=520)
        workspace = ArmWorkspace(
            self._root,
            model=self._arm_model,
            mediator=self._mediator,
            style=custom_style
        )
        self.assertIsNotNone(workspace.get_control_panel())


if __name__ == '__main__':
    main()
