# -*- coding: UTF-8 -*-

'''
Module
    mecha_editor_toolbar.py
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
    Toolbar component housing action buttons and example selector for Mecha DSL editor.
'''

from __future__ import annotations

from tkinter import Button, Frame, LEFT, RIGHT, Widget, X
from tkinter.ttk import Combobox
from typing import Callable

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.dsl.mecha_example_catalog import MechaExampleCatalog

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaEditorToolbar(Frame):
    '''
        Toolbar presenting document actions, compiler controls, and example selector.

        It defines:

            :methods:
                | __init__ - Initializes toolbar with action buttons and styling.
                | set_running_state - Updates button states when execution starts/stops.
    '''

    _btn_run: Button
    _btn_stop: Button

    def __init__(
        self,
        parent: Widget,
        on_new: Callable[[], None],
        on_open: Callable[[], None],
        on_save: Callable[[], None],
        on_example_selected: Callable[[str], None],
        on_validate: Callable[[], None],
        on_compile: Callable[[], None],
        on_run: Callable[[], None],
        on_stop: Callable[[], None],
        **kwargs: object
    ) -> None:
        '''
            Configures action buttons and example selection dropdown.

            :param parent: Parent Tkinter widget.
            :param on_new: New file handler.
            :param on_open: Open file handler.
            :param on_save: Save file handler.
            :param on_example_selected: Demo selection handler.
            :param on_validate: Validation handler.
            :param on_compile: Compile handler.
            :param on_run: Run streaming handler.
            :param on_stop: Stop streaming handler.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER, bd=0, padx=6, pady=4, **kwargs)

        self._create_btn('📄 New', on_new)
        self._create_btn('📂 Open', on_open)
        self._create_btn('💾 Save', on_save)

        # Example catalog dropdown
        combo = Combobox(
            self,
            values=MechaExampleCatalog.get_example_names(),
            state='readonly',
            width=20
        )
        combo.set('📚 Load Example...')
        combo.pack(side=LEFT, padx=6)
        combo.bind(
            '<<ComboboxSelected>>',
            lambda _e: on_example_selected(combo.get())
        )

        self._create_btn('🔍 Validate', on_validate, bg=ThemeManager.BG_CARD)
        self._create_btn('⚙️ Compile', on_compile, bg=ThemeManager.BG_CARD)

        self._btn_stop = self._create_btn(
            '⏹️ Stop',
            on_stop,
            side=RIGHT,
            bg=ThemeManager.ACCENT_RED,
            fg='#11111b'
        )
        self._btn_run = self._create_btn(
            '▶️ Run',
            on_run,
            side=RIGHT,
            bg=ThemeManager.ACCENT_GREEN,
            fg='#11111b'
        )

    def _create_btn(
        self,
        text: str,
        cmd: Callable[[], None],
        side: str = LEFT,
        bg: str = ThemeManager.BG_PANEL,
        fg: str = ThemeManager.TEXT_PRIMARY
    ) -> Button:
        '''Helper constructing a styled toolbar button.'''
        btn = Button(
            self,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            activebackground=ThemeManager.ACCENT_BLUE,
            activeforeground='#11111b',
            relief='flat',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=8,
            pady=2,
            bd=0
        )
        btn.pack(side=side, padx=3)
        return btn

    def set_running_state(self, is_running: bool) -> None:
        '''Updates visual state of Run and Stop buttons.'''
        if is_running:
            self._btn_run.config(state='disabled')
            self._btn_stop.config(state='normal')
        else:
            self._btn_run.config(state='normal')
            self._btn_stop.config(state='normal')
