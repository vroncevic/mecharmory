# -*- coding: UTF-8 -*-

'''
Module
    serial_port_selector.py
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
    Serial port discovery and baudrate dropdown selector toolbar component.
'''

from __future__ import annotations

from tkinter import FLAT, LEFT, Button, Frame, Label, Widget
from tkinter.ttk import Combobox

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.serial.serial_panel_style import (
    SerialPanelStyle
)
from mecharmory.infrastructure.communication.iserial_port_scanner import (
    ISerialPortScanner
)
from mecharmory.infrastructure.communication.iserial_preferences import (
    ISerialPreferences
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortSelector(Frame):
    '''
        Encapsulates port dropdown, Scan action, and baudrate selection.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _port_combo - Dropdown combobox for available ports.
                | _baud_combo - Dropdown combobox for baudrate choices.
                | _scanner - Port discovery interface.
                | _preferences - Configuration storage interface.
                | _style - Visual styling configuration reference.
            :methods:
                | __init__ - Builds port and baudrate widgets.
                | refresh_ports - Scans ports and selects preference.
                | get_selected_port - Returns currently selected port string.
                | get_selected_baudrate - Returns integer baudrate.
                | save_preference - Persists current selection to preferences.
    '''

    DEFAULT_STYLE: SerialPanelStyle = SerialPanelStyle()

    _port_combo: Combobox
    _baud_combo: Combobox
    _scanner: ISerialPortScanner
    _preferences: ISerialPreferences
    _style: SerialPanelStyle

    def __init__(
        self,
        parent: Widget,
        scanner: ISerialPortScanner,
        preferences: ISerialPreferences,
        style: SerialPanelStyle | None = None
    ) -> None:
        '''
            Initializes port and baudrate selector controls.

            :param parent: Parent container widget.
            :param scanner: ISerialPortScanner interface.
            :param preferences: ISerialPreferences interface.
            :param style: Optional visual styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER)
        cfg: SerialPanelStyle = style or self.DEFAULT_STYLE
        self._style = cfg
        self._scanner = scanner
        self._preferences = preferences

        # Port Selector
        lbl_port = Label(
            self,
            text=cfg.port_label_text,
            font=(ThemeManager.FONT_FAMILY, cfg.label_font_size),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_HEADER
        )
        lbl_port.pack(side=LEFT, padx=cfg.label_pad_x)

        self._port_combo = Combobox(
            self,
            width=cfg.port_combo_width,
            state=cfg.combo_state
        )
        self._port_combo.pack(side=LEFT, padx=cfg.combo_pad_x)

        btn_scan = Button(
            self,
            text=cfg.btn_scan_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_scan_font_size),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=cfg.btn_scan_pad_x,
            pady=cfg.btn_scan_pad_y,
            command=self.refresh_ports
        )
        btn_scan.pack(side=LEFT, padx=cfg.btn_scan_spacing_x)

        # Baudrate Selector
        lbl_baud = Label(
            self,
            text=cfg.baud_label_text,
            font=(ThemeManager.FONT_FAMILY, cfg.label_font_size),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_HEADER
        )
        lbl_baud.pack(side=LEFT, padx=cfg.label_pad_x)

        self._baud_combo = Combobox(
            self,
            width=cfg.baud_combo_width,
            values=[str(b) for b in cfg.baudrates],
            state=cfg.combo_state
        )
        self._baud_combo.set(str(cfg.default_baud))
        self._baud_combo.pack(side=LEFT, padx=cfg.baud_combo_spacing_x)

        self.refresh_ports()

    def refresh_ports(self) -> None:
        '''
            Discovers serial ports and selects saved preference.
        '''
        saved_port, saved_baud = self._preferences.load_preference()
        ports: list[str] = self._scanner.get_available_ports()
        if not ports:
            ports = list(self._style.fallback_ports)

        self._port_combo['values'] = ports
        if saved_port in ports:
            self._port_combo.set(saved_port)
        elif ports:
            self._port_combo.set(ports[0])

        self._baud_combo.set(str(saved_baud))

    def get_selected_port(self) -> str:
        '''
            Returns active port choice.

            :return: Port name string.
        '''
        return self._port_combo.get()

    def get_selected_baudrate(self) -> int:
        '''
            Returns active baudrate choice.

            :return: Baudrate integer.
        '''
        try:
            return int(self._baud_combo.get())
        except ValueError:
            return self.DEFAULT_STYLE.default_baud

    def save_preference(self) -> None:
        '''
            Saves selected port and baudrate to user preferences.
        '''
        self._preferences.save_preference(
            self.get_selected_port(),
            self.get_selected_baudrate()
        )
