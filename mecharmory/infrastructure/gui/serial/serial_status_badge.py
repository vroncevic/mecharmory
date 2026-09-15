# -*- coding: UTF-8 -*-

'''
Module
    serial_status_badge.py
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
    Connection status indicator badge and connect/disconnect action button.
'''

from __future__ import annotations

from tkinter import FLAT, Button, Label, Widget
from typing import Callable

from mecharmory.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialStatusBadge:
    '''
        Visual connection status badge and connect/disconnect trigger button.

        It defines:

            :attributes:
                | _btn_connect - Connect / Disconnect button.
                | _lbl_status - Real-time connection status label.
            :methods:
                | __init__ - Builds connect button and status label.
                | set_connected_state - Updates visual state and colors.
                | get_button - Accesses connect button instance.
                | get_label - Accesses status label instance.
    '''

    _btn_connect: Button
    _lbl_status: Label

    def __init__(
        self,
        parent: Widget,
        on_connect_click: Callable[[], None]
    ) -> None:
        '''
            Initializes connect button and status label.

            :param parent: Parent container widget.
            :param on_connect_click: Connect click action handler.
        '''
        self._btn_connect = Button(
            parent,
            text='Connect',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            bg=ThemeManager.ACCENT_GREEN,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=14,
            pady=3,
            command=on_connect_click
        )

        self._lbl_status = Label(
            parent,
            text='Offline',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            fg=ThemeManager.ACCENT_RED,
            bg=ThemeManager.BG_HEADER
        )

    def set_connected_state(self, connected: bool, desc: str) -> None:
        '''
            Updates visual state of connect button and status text.

            :param connected: True if connected.
            :param desc: Status description string.
        '''
        if connected:
            self._btn_connect.config(
                text='Disconnect',
                bg=ThemeManager.ACCENT_RED,
                fg='#ffffff'
            )
            self._lbl_status.config(
                text=desc,
                fg=ThemeManager.ACCENT_GREEN
            )
        else:
            self._btn_connect.config(
                text='Connect',
                bg=ThemeManager.ACCENT_GREEN,
                fg=ThemeManager.BG_DARK
            )
            self._lbl_status.config(
                text='Disconnected',
                fg=ThemeManager.ACCENT_RED
            )

    def get_button(self) -> Button:
        '''
            Returns connect button widget.

            :return: Button widget.
        '''
        return self._btn_connect

    def get_label(self) -> Label:
        '''
            Returns status badge label widget.

            :return: Label widget.
        '''
        return self._lbl_status
