# -*- coding: UTF-8 -*-

'''
Module
    arm_control_header.py
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
    Header toolbar displaying joint controls title and global arm action buttons.
'''

from __future__ import annotations

from typing import Callable, Final
from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    Button,
    Frame,
    Label,
    Widget
)

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.arm.arm_panel_style import ArmPanelStyle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmControlHeader(Frame):
    '''
        Header bar managing manipulator global actions and section title.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _on_status - Callback for status inquiry.
                | _on_home - Callback for homing sequence.
                | _on_stop - Callback for emergency stop.
                | _lbl_section - Title Label component.
                | _btn_stop - Emergency Stop Button component.
                | _btn_home - Home All Button component.
                | _btn_query - Query Status Button component.
            :methods:
                | __init__ - Configures title and global action buttons.
    '''

    DEFAULT_STYLE: Final[ArmPanelStyle] = ArmPanelStyle()

    _on_status: Callable[[], None]
    _on_home: Callable[[], None]
    _on_stop: Callable[[], None]
    _lbl_section: Label
    _btn_stop: Button
    _btn_home: Button
    _btn_query: Button

    def __init__(
        self,
        parent: Widget,
        on_status: Callable[[], None],
        on_home: Callable[[], None],
        on_stop: Callable[[], None],
        style: ArmPanelStyle | None = None
    ) -> None:
        '''
            Initializes arm control header toolbar.

            :param parent: Parent container widget.
            :param on_status: Status query callback.
            :param on_home: Homing callback.
            :param on_stop: Emergency stop callback.
            :param style: Optional styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        cfg: ArmPanelStyle = style or self.DEFAULT_STYLE
        self._on_status = on_status
        self._on_home = on_home
        self._on_stop = on_stop

        self._lbl_section = Label(
            self,
            text=cfg.title_text,
            font=(ThemeManager.FONT_FAMILY, cfg.title_font_size, cfg.title_font_weight),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        self._lbl_section.pack(side=LEFT)

        # Stop Button (Far Right)
        self._btn_stop = Button(
            self,
            text=cfg.btn_stop_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_stop_font_size, cfg.btn_font_weight),
            bg=ThemeManager.ACCENT_RED,
            fg=cfg.btn_stop_fg,
            relief=FLAT,
            padx=cfg.btn_stop_pad_x,
            pady=cfg.btn_stop_pad_y,
            command=self._on_stop
        )
        self._btn_stop.pack(side=RIGHT, padx=cfg.btn_spacing_x)

        # Home Button
        self._btn_home = Button(
            self,
            text=cfg.btn_home_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_home_font_size, cfg.btn_font_weight),
            bg=ThemeManager.ACCENT_BLUE,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=cfg.btn_home_pad_x,
            pady=cfg.btn_home_pad_y,
            command=self._on_home
        )
        self._btn_home.pack(side=RIGHT, padx=cfg.btn_spacing_x)

        # Query Status Button
        self._btn_query = Button(
            self,
            text=cfg.btn_query_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_query_font_size),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=cfg.btn_query_pad_x,
            pady=cfg.btn_query_pad_y,
            command=self._on_status
        )
        self._btn_query.pack(side=RIGHT)
