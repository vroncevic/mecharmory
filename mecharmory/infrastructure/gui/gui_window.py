# -*- coding: UTF-8 -*-

'''
Module
    gui_window.py
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
    Desktop application window coordinating UI layout and event polling.
'''

from __future__ import annotations

from queue import Queue, Empty
from typing import Final
from tkinter import BOTH, BOTTOM, TOP, X, Frame, Tk
from tkinter.ttk import Notebook

from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.core.service.arm.iarm_controller_service import (
    IArmControllerService
)
from mecharmory.core.service.serial.iserial_service import ISerialService
from mecharmory.infrastructure.communication.iserial_preferences import (
    ISerialPreferences
)
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.gui_event_mediator import GuiEventMediator
from mecharmory.infrastructure.gui.gui_window_style import GuiWindowStyle
from mecharmory.infrastructure.gui.serial.serial_bar import SerialBar
from mecharmory.infrastructure.gui.workspace.arm_workspace import ArmWorkspace
from mecharmory.infrastructure.gui.console.console_panel import ConsolePanel
from mecharmory.infrastructure.gui.dsl.mecha_editor_tab import MechaEditorTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiWindow:
    '''
        Master UI application window managing components and coordinating layout.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default GuiWindowStyle metrics and parameters.
                | _style - Active GuiWindowStyle styling configuration.
                | _root - Main Tkinter application window instance.
                | _arm_service - Manipulator coordination service interface.
                | _serial_service - Communication bridge service interface.
                | _preferences - Optional serial preferences interface.
                | _ui_queue - Thread-safe inter-thread message queue.
                | _mediator - GuiEventMediator delegating UI events.
                | _serial_bar - Serial connection toolbar component.
                | _workspace - Arm workspace component containing controls and canvas.
                | _console_panel - Console logging and command entry subpanel.
                | _is_running - Flag indicating whether event loop is active.
            :methods:
                | __init__ - Initializes window layout and subpanels.
                | is_initialized - Confirms operational readiness of window.
                | start - Starts Tkinter event loop.
                | stop - Terminates application window cleanly.
                | is_running - Queries whether application event loop is executing.
    '''

    DEFAULT_STYLE: Final[GuiWindowStyle] = GuiWindowStyle()
    _style: GuiWindowStyle
    _root: Tk
    _arm_service: IArmControllerService
    _serial_service: ISerialService
    _preferences: ISerialPreferences | None
    _ui_queue: Queue[SerialMessage]
    _mediator: GuiEventMediator
    _serial_bar: SerialBar
    _workspace: ArmWorkspace
    _editor_tab: MechaEditorTab
    _console_panel: ConsolePanel
    _is_running: bool

    def __init__(
        self,
        arm_service: IArmControllerService,
        serial_service: ISerialService,
        preferences: ISerialPreferences | None = None,
        style: GuiWindowStyle | None = None
    ) -> None:
        '''
            Initializes window layout and subpanels.

            :param arm_service: Manipulator coordination service interface.
            :param serial_service: Communication bridge service interface.
            :param preferences: Optional serial preferences interface.
            :param style: Optional window layout configuration.
        '''
        self._style = style or self.DEFAULT_STYLE
        self._arm_service = arm_service
        self._serial_service = serial_service
        self._preferences = preferences
        self._ui_queue = Queue()
        self._is_running = False

        self._mediator = GuiEventMediator(
            self._arm_service,
            self._serial_service,
            self._ui_queue
        )

        self._root = Tk()
        self._root.title(self._style.window_title)
        self._root.geometry(self._style.window_geometry)
        self._root.resizable(False, False)
        self._root.configure(bg=ThemeManager.BG_DARK)

        self._setup_views()
        self._bind_services()

    def is_initialized(self) -> bool:
        '''
            Confirms operational readiness of window.

            :return: True if root and services are initialized.
        '''
        return (
            self._root is not None
            and self._arm_service is not None
            and self._serial_service is not None
        )

    def start(self) -> None:
        '''Starts main event loop.'''
        self._is_running = True
        self._root.after(self._style.poll_interval_ms, self._periodic_ui_poll)
        self._root.mainloop()

    def stop(self) -> None:
        '''Terminates window.'''
        self._is_running = False
        self._serial_service.disconnect()

        try:
            self._root.destroy()

        except Exception:
            pass

    def is_running(self) -> bool:
        '''Queries running state.'''
        return self._is_running

    def _setup_views(self) -> None:
        '''Builds layout containers and child widgets.'''
        self._serial_bar = SerialBar(
            self._root,
            on_connect_toggle=self._mediator.on_connect_toggle,
            on_virtual_toggle=self._mediator.on_virtual_toggle,
            on_ping=self._mediator.on_ping,
            preferences=self._preferences
        )
        self._serial_bar.pack(fill=X, side=TOP)

        body = Frame(
            self._root,
            bg=ThemeManager.BG_DARK,
            padx=self._style.body_pad_x,
            pady=self._style.body_pad_y
        )
        body.pack(fill=BOTH, expand=True, side=TOP)

        self._console_panel = ConsolePanel(body, on_send=self._mediator.on_manual_command)
        self._console_panel.pack(fill=X, side=BOTTOM)

        notebook = Notebook(body)
        self._workspace = ArmWorkspace(
            notebook,
            model=self._arm_service.get_model(),
            mediator=self._mediator,
            style=self._style
        )
        self._editor_tab = MechaEditorTab(
            notebook,
            on_send_command=self._mediator.on_manual_command,
            model=self._arm_service.get_model()
        )
        notebook.add(self._workspace, text='  🎮 Manual Workspace  ')
        notebook.add(self._editor_tab, text='  📝 Mecha Script Editor  ')
        notebook.pack(
            fill=BOTH,
            expand=True,
            side=TOP,
            pady=self._style.upper_row_spacing_y
        )

        self._root.protocol(self._style.protocol_delete_window, self.stop)

    def get_editor_tab(self) -> MechaEditorTab:
        '''
            Returns internal MechaEditorTab reference.

            :return: MechaEditorTab instance.
        '''
        return self._editor_tab

    def _bind_services(self) -> None:
        '''Binds background notification callbacks.'''
        self._serial_service.register_rx_callback(self._mediator.on_serial_rx)
        self._serial_service.register_status_callback(
            self._serial_bar.set_connected_state
        )

    def _periodic_ui_poll(self) -> None:
        '''Main-thread periodic poll draining communication queue and updating visuals.'''
        if not self._is_running:
            return

        self._drain_ui_queue()

        if self._serial_service.is_connected():
            self._arm_service.query_status()

        self._workspace.refresh_visuals()
        self._root.after(self._style.poll_interval_ms, self._periodic_ui_poll)

    def _drain_ui_queue(self) -> None:
        '''Drains serial communication queue and outputs messages to console.'''
        try:
            while True:
                msg: SerialMessage = self._ui_queue.get_nowait()
                self._console_panel.append_message(msg)

        except Empty:
            pass
