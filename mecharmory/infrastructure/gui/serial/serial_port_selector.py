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

from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.communication.iserial_port_scanner import ISerialPortScanner
from mecharmory.infrastructure.communication.iserial_preferences import ISerialPreferences

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
                | _port_combo - Port dropdown selection widget.
                | _baud_combo - Baudrate dropdown selection widget.
                | _scanner - ISerialPortScanner interface.
                | _preferences - ISerialPreferences interface.
            :methods:
                | __init__ - Builds port and baudrate widgets.
                | refresh_ports - Scans ports and selects preference.
                | get_selected_port - Returns currently selected port string.
                | get_selected_baudrate - Returns integer baudrate.
                | save_preference - Persists current selection to preferences.
    '''

    _port_combo: Combobox
    _baud_combo: Combobox
    _scanner: ISerialPortScanner
    _preferences: ISerialPreferences

    def __init__(
        self,
        parent: Widget,
        scanner: ISerialPortScanner,
        preferences: ISerialPreferences
    ) -> None:
        '''
            Initializes port and baudrate selector controls.

            :param parent: Parent container widget.
            :param scanner: ISerialPortScanner interface.
            :param preferences: ISerialPreferences interface.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER)
        self._scanner = scanner
        self._preferences = preferences

        # Port Selector
        lbl_port = Label(
            self,
            text='Port:',
            font=(ThemeManager.FONT_FAMILY, 9),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_HEADER
        )
        lbl_port.pack(side=LEFT, padx=(0, 4))

        self._port_combo = Combobox(self, width=15, state='readonly')
        self._port_combo.pack(side=LEFT, padx=(0, 6))

        btn_scan = Button(
            self,
            text='Scan',
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=8,
            pady=2,
            command=self.refresh_ports
        )
        btn_scan.pack(side=LEFT, padx=(0, 12))

        # Baudrate Selector
        lbl_baud = Label(
            self,
            text='Baud:',
            font=(ThemeManager.FONT_FAMILY, 9),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_HEADER
        )
        lbl_baud.pack(side=LEFT, padx=(0, 4))

        self._baud_combo = Combobox(
            self,
            width=8,
            values=('9600', '19200', '38400', '57600', '115200', '230400', '921600'),
            state='readonly'
        )
        self._baud_combo.set('115200')
        self._baud_combo.pack(side=LEFT, padx=(0, 12))

        self.refresh_ports()

    def refresh_ports(self) -> None:
        '''
            Discovers serial ports and selects saved preference.
        '''
        saved_port, saved_baud = self._preferences.load_preference()
        ports: list[str] = self._scanner.get_available_ports()
        if not ports:
            ports = ['/dev/ttyACM0', '/dev/ttyUSB0']

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
            return 115200

    def save_preference(self) -> None:
        '''
            Saves selected port and baudrate to user preferences.
        '''
        self._preferences.save_preference(
            self.get_selected_port(),
            self.get_selected_baudrate()
        )
