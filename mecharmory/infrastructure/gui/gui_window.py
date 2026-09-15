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
from tkinter import (
    BOTH,
    LEFT,
    RIGHT,
    TOP,
    X,
    Frame,
    Tk
)
from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.core.service.arm.iarm_controller_service import (
    IArmControllerService
)
from mecharmory.core.service.serial.iserial_service import ISerialService
from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.gui.gui_event_mediator import GuiEventMediator
from mecharmory.infrastructure.gui.serial.serial_bar import SerialBar
from mecharmory.infrastructure.gui.arm.arm_control_panel import ArmControlPanel
from mecharmory.infrastructure.gui.preset.preset_panel import PresetPanel
from mecharmory.infrastructure.gui.canvas.arm_canvas_preview import (
    ArmCanvasPreview
)
from mecharmory.infrastructure.gui.console.console_panel import ConsolePanel

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
                | _root - Primary Tkinter root window.
                | _arm_service - IArmControllerService instance.
                | _serial_service - ISerialService instance.
                | _ui_queue - Queue decoupling background serial threads from Tkinter main thread.
                | _mediator - GuiEventMediator coordinating events.
                | _serial_bar - Top connection toolbar.
                | _control_panel - Joint sliders and global action panel.
                | _preset_panel - Posture presets toolbar.
                | _canvas_preview - 2D kinematic schematic visualizer.
                | _console_panel - Serial monitor and input console.
                | _is_running - Window display flag.
            :methods:
                | __init__ - Configures layouts, frames, and event bindings.
                | is_initialized - Confirms operational readiness of window.
                | start - Enters Tkinter main event loop.
                | stop - Terminates application.
                | is_running - Queries lifecycle state.
    '''

    _root: Tk
    _arm_service: IArmControllerService
    _serial_service: ISerialService
    _ui_queue: Queue[SerialMessage]
    _mediator: GuiEventMediator
    _serial_bar: SerialBar
    _control_panel: ArmControlPanel
    _preset_panel: PresetPanel
    _canvas_preview: ArmCanvasPreview
    _console_panel: ConsolePanel
    _is_running: bool

    def __init__(
        self,
        arm_service: IArmControllerService,
        serial_service: ISerialService
    ) -> None:
        '''
            Initializes window layout and subpanels.

            :param arm_service: Manipulator coordination service interface.
            :param serial_service: Communication bridge service interface.
        '''
        self._arm_service = arm_service
        self._serial_service = serial_service
        self._ui_queue = Queue()
        self._is_running = False

        self._mediator = GuiEventMediator(
            self._arm_service,
            self._serial_service,
            self._ui_queue
        )

        self._root = Tk()
        self._root.title('Mecharmory - 6-DOF Robotic Arm Studio')
        self._root.geometry('1120x760')
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
        self._root.after(40, self._periodic_ui_poll)
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
        # Top Serial Bar
        self._serial_bar = SerialBar(
            self._root,
            on_connect_toggle=self._mediator.on_connect_toggle,
            on_virtual_toggle=self._mediator.on_virtual_toggle,
            on_ping=self._mediator.on_ping
        )
        self._serial_bar.pack(fill=X, side=TOP)

        # Center Body Frame
        body = Frame(self._root, bg=ThemeManager.BG_DARK, padx=10, pady=8)
        body.pack(fill=BOTH, expand=True, side=TOP)

        # Left Column: Joint Controls and Presets
        left_col = Frame(body, bg=ThemeManager.BG_DARK)
        left_col.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        self._control_panel = ArmControlPanel(
            left_col,
            model=self._arm_service.get_model(),
            on_joint_command=self._mediator.on_joint_move,
            on_home=self._mediator.on_home,
            on_stop=self._mediator.on_stop,
            on_status=self._mediator.on_query_status
        )
        self._control_panel.pack(fill=X, side=TOP, pady=(0, 8))

        self._preset_panel = PresetPanel(
            left_col,
            presets=self._arm_service.get_model().get_presets(),
            on_apply_preset=self._mediator.on_apply_preset
        )
        self._preset_panel.pack(fill=X, side=TOP)

        # Right Column: Live 2D Preview and Serial Console
        right_col = Frame(body, bg=ThemeManager.BG_DARK, width=380)
        right_col.pack(side=RIGHT, fill=BOTH, expand=False)
        right_col.pack_propagate(False)

        self._canvas_preview = ArmCanvasPreview(
            right_col,
            model=self._arm_service.get_model()
        )
        self._canvas_preview.pack(fill=X, side=TOP, pady=(0, 8))

        self._console_panel = ConsolePanel(
            right_col,
            on_send=self._mediator.on_manual_command
        )
        self._console_panel.pack(fill=BOTH, expand=True, side=TOP)

        self._root.protocol('WM_DELETE_WINDOW', self.stop)

    def _bind_services(self) -> None:
        '''Binds background notification callbacks.'''
        self._serial_service.register_rx_callback(self._mediator.on_serial_rx)
        self._serial_service.register_status_callback(self._serial_bar.set_connected_state)

    def _periodic_ui_poll(self) -> None:
        '''Main-thread periodic poll draining communication queue and updating visuals.'''
        if not self._is_running:
            return

        try:
            while True:
                msg: SerialMessage = self._ui_queue.get_nowait()
                self._console_panel.append_message(msg)
        except Empty:
            pass

        # Periodic query if connected
        if self._serial_service.is_connected():
            self._arm_service.query_status()

        self._canvas_preview.update_pose()
        self._control_panel.refresh_telemetry()

        self._root.after(40, self._periodic_ui_poll)
