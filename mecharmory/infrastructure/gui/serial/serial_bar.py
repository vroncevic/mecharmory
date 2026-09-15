# -*- coding: UTF-8 -*-

'''
Module
    serial_bar.py
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
    Top toolbar component for serial communication bridge configuration.
'''

from __future__ import annotations

from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    Button,
    Checkbutton,
    Frame,
    Label,
    BooleanVar,
    Widget
)
from typing import Callable

from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from mecharmory.infrastructure.communication.iserial_preferences import ISerialPreferences
from mecharmory.infrastructure.communication.serial_port_scanner import SerialPortScanner
from mecharmory.infrastructure.communication.serial_preferences import SerialPreferences
from mecharmory.infrastructure.gui.serial.serial_port_selector import (
    SerialPortSelector
)
from mecharmory.infrastructure.gui.serial.serial_status_badge import (
    SerialStatusBadge
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialBar(Frame):
    '''
        Toolbar for scanning ports, selecting baudrate, and managing connection lifecycle.

        It defines:

            :attributes:
                | _selector - SerialPortSelector sub-widget.
                | _badge - SerialStatusBadge sub-widget.
                | _virtual_var - Virtual mode toggle state variable.
                | _on_connect_toggle - Callback for connection request.
                | _on_virtual_toggle - Callback for virtual mode toggle.
                | _on_ping - Callback for heartbeat ping.
            :methods:
                | __init__ - Configures and packs UI widgets.
                | refresh_ports - Scans system serial ports.
                | set_connected_state - Updates button appearance and status badge.
                | _handle_connect_click - Dispatches connection toggle.
                | _handle_virtual_toggle - Dispatches virtual mode switch.
                | _handle_ping_click - Dispatches heartbeat ping.
    '''

    _selector: SerialPortSelector
    _badge: SerialStatusBadge
    _virtual_var: BooleanVar
    _on_connect_toggle: Callable[[str, int], None] | None
    _on_virtual_toggle: Callable[[bool], None] | None
    _on_ping: Callable[[], None] | None

    def __init__(
        self,
        parent: Widget,
        on_connect_toggle: Callable[[str, int], None] | None = None,
        on_virtual_toggle: Callable[[bool], None] | None = None,
        on_ping: Callable[[], None] | None = None,
        scanner: ISerialPortScanner | None = None,
        preferences: ISerialPreferences | None = None
    ) -> None:
        '''
            Initializes serial toolbar widgets.

            :param parent: Parent container widget.
            :param on_connect_toggle: Connect callback.
            :param on_virtual_toggle: Virtual mode callback.
            :param on_ping: Ping heartbeat callback.
            :param scanner: Optional port scanner abstraction.
            :param preferences: Optional serial preferences abstraction.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER, height=44, padx=12, pady=6)
        self._on_connect_toggle = on_connect_toggle
        self._on_virtual_toggle = on_virtual_toggle
        self._on_ping = on_ping

        port_scanner: ISerialPortScanner = scanner or SerialPortScanner()
        user_prefs: ISerialPreferences = preferences or SerialPreferences()

        # Title Label
        lbl_title = Label(
            self,
            text='Mecharmo 6-DOF',
            font=(ThemeManager.FONT_FAMILY, 11, 'bold'),
            fg=ThemeManager.ACCENT_CYAN,
            bg=ThemeManager.BG_HEADER
        )
        lbl_title.pack(side=LEFT, padx=(0, 15))

        # Port and Baudrate Selector
        self._selector = SerialPortSelector(self, port_scanner, user_prefs)
        self._selector.pack(side=LEFT)

        # Status Badge & Connect Button
        self._badge = SerialStatusBadge(self, self._handle_connect_click)
        self._badge.get_button().pack(side=LEFT, padx=(0, 12))

        # Virtual Emulation Toggle
        self._virtual_var = BooleanVar(value=False)
        chk_virtual = Checkbutton(
            self,
            text='Virtual Firmware Mode',
            variable=self._virtual_var,
            font=(ThemeManager.FONT_FAMILY, 9),
            fg=ThemeManager.ACCENT_YELLOW,
            bg=ThemeManager.BG_HEADER,
            selectcolor=ThemeManager.BG_DARK,
            activebackground=ThemeManager.BG_HEADER,
            activeforeground=ThemeManager.ACCENT_YELLOW,
            command=self._handle_virtual_toggle
        )
        chk_virtual.pack(side=LEFT, padx=(0, 12))

        # Ping Button
        btn_ping = Button(
            self,
            text='Ping',
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_BLUE,
            relief=FLAT,
            padx=8,
            pady=2,
            command=self._handle_ping_click
        )
        btn_ping.pack(side=LEFT, padx=(0, 12))

        # Status Badge Label
        self._badge.get_label().pack(side=RIGHT, padx=6)

    def refresh_ports(self) -> None:
        '''
            Discovers serial ports and selects preference.
        '''
        self._selector.refresh_ports()

    def set_connected_state(self, connected: bool, desc: str) -> None:
        '''
            Updates visual state of connect button and status text.

            :param connected: True if connected.
            :param desc: Status description string.
        '''
        self._badge.set_connected_state(connected, desc)

    def _handle_connect_click(self) -> None:
        '''
            Dispatches connect toggle.
        '''
        if self._on_connect_toggle is not None:
            self._selector.save_preference()
            self._on_connect_toggle(
                self._selector.get_selected_port(),
                self._selector.get_selected_baudrate()
            )

    def _handle_virtual_toggle(self) -> None:
        '''
            Dispatches virtual mode switch.
        '''
        if self._on_virtual_toggle is not None:
            self._on_virtual_toggle(self._virtual_var.get())

    def _handle_ping_click(self) -> None:
        '''
            Dispatches heartbeat ping.
        '''
        if self._on_ping is not None:
            self._on_ping()
