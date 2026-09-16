# -*- coding: UTF-8 -*-

'''
Module
    console_header_toolbar.py
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
    Header toolbar for serial monitor and command console with action buttons.
'''

from __future__ import annotations

from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    Button,
    Frame,
    Label,
    Widget
)
from typing import Callable

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.console.console_panel_style import (
    ConsolePanelStyle
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConsoleHeaderToolbar(Frame):
    '''
        Header bar displaying console title and action buttons.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _on_clear - Callback invoked when Clear is clicked.
                | _on_copy - Callback invoked when Copy is clicked.
                | _on_select_all - Callback invoked when Select All is clicked.
                | _lbl_title - Title Label widget.
                | _btn_clear - Clear Button widget.
                | _btn_copy - Copy Button widget.
                | _btn_select_all - Select All Button widget.
            :methods:
                | __init__ - Configures header labels and action buttons.
    '''

    DEFAULT_STYLE: ConsolePanelStyle = ConsolePanelStyle()

    _on_clear: Callable[[], None]
    _on_copy: Callable[[], None]
    _on_select_all: Callable[[], None]
    _lbl_title: Label
    _btn_clear: Button
    _btn_copy: Button
    _btn_select_all: Button

    def __init__(
        self,
        parent: Widget,
        on_clear: Callable[[], None],
        on_copy: Callable[[], None],
        on_select_all: Callable[[], None],
        style: ConsolePanelStyle | None = None
    ) -> None:
        '''
            Initializes console header toolbar.

            :param parent: Parent Tkinter widget.
            :param on_clear: Callback invoked on clear action.
            :param on_copy: Callback invoked on copy action.
            :param on_select_all: Callback invoked on select-all action.
            :param style: Optional visual styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        cfg: ConsolePanelStyle = style or self.DEFAULT_STYLE
        self._on_clear = on_clear
        self._on_copy = on_copy
        self._on_select_all = on_select_all

        self._lbl_title = Label(
            self,
            text=cfg.title_text,
            font=(ThemeManager.FONT_FAMILY, cfg.title_font_size, 'bold'),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        self._lbl_title.pack(side=LEFT)

        self._btn_clear = Button(
            self,
            text=cfg.btn_clear_text,
            font=(ThemeManager.FONT_FAMILY, cfg.action_btn_font_size),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_SECONDARY,
            relief=FLAT,
            padx=cfg.action_btn_pad_x,
            pady=cfg.action_btn_pad_y,
            command=self._on_clear
        )
        self._btn_clear.pack(side=RIGHT)

        self._btn_copy = Button(
            self,
            text=cfg.btn_copy_text,
            font=(ThemeManager.FONT_FAMILY, cfg.action_btn_font_size),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_SECONDARY,
            relief=FLAT,
            padx=cfg.action_btn_pad_x,
            pady=cfg.action_btn_pad_y,
            command=self._on_copy
        )
        self._btn_copy.pack(side=RIGHT, padx=cfg.action_btn_spacing_x)

        self._btn_select_all = Button(
            self,
            text=cfg.btn_select_all_text,
            font=(ThemeManager.FONT_FAMILY, cfg.action_btn_font_size),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_SECONDARY,
            relief=FLAT,
            padx=cfg.action_btn_pad_x,
            pady=cfg.action_btn_pad_y,
            command=self._on_select_all
        )
        self._btn_select_all.pack(side=RIGHT, padx=cfg.action_btn_spacing_x)
