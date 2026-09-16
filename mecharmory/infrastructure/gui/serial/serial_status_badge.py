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
    Status badge and connection toggle button for serial toolbar.
'''

from __future__ import annotations

from tkinter import FLAT, Button, Label, Widget
from typing import Callable

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.serial.serial_panel_style import (
    SerialPanelStyle
)

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
                | DEFAULT_STYLE - Default visual styling parameters.
                | _style - SerialPanelStyle configuration reference.
                | _btn_connect - Connect / Disconnect button.
                | _lbl_status - Real-time connection status label.
            :methods:
                | __init__ - Builds connect button and status label.
                | set_connected_state - Updates visual state and colors.
                | get_button - Accesses connect button instance.
                | get_label - Accesses status label instance.
    '''

    DEFAULT_STYLE: SerialPanelStyle = SerialPanelStyle()

    _style: SerialPanelStyle
    _btn_connect: Button
    _lbl_status: Label

    def __init__(
        self,
        parent: Widget,
        on_connect_click: Callable[[], None],
        style: SerialPanelStyle | None = None
    ) -> None:
        '''
            Initializes connect button and status label.

            :param parent: Parent container widget.
            :param on_connect_click: Connect click action handler.
            :param style: Optional visual styling configuration.
        '''
        self._style = style or self.DEFAULT_STYLE
        self._btn_connect = Button(
            parent,
            text=self._style.btn_connect_text,
            font=(ThemeManager.FONT_FAMILY, self._style.badge_font_size, 'bold'),
            bg=ThemeManager.ACCENT_GREEN,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=self._style.badge_pad_x,
            pady=self._style.badge_pad_y,
            command=on_connect_click
        )

        self._lbl_status = Label(
            parent,
            text=self._style.status_offline_text,
            font=(ThemeManager.FONT_FAMILY, self._style.badge_font_size, 'bold'),
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
                text=self._style.btn_disconnect_text,
                bg=ThemeManager.ACCENT_RED,
                fg=self._style.btn_disconnect_fg
            )
            self._lbl_status.config(
                text=desc,
                fg=ThemeManager.ACCENT_GREEN
            )
        else:
            self._btn_connect.config(
                text=self._style.btn_connect_text,
                bg=ThemeManager.ACCENT_GREEN,
                fg=ThemeManager.BG_DARK
            )
            self._lbl_status.config(
                text=self._style.status_disconnected_text,
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
