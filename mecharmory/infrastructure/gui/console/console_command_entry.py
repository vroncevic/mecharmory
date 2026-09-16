# -*- coding: UTF-8 -*-

'''
Module
    console_command_entry.py
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
    Command prompt and direct ASCII instruction submission row.
'''

from __future__ import annotations

from typing import Callable, Final
from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    X,
    Button,
    Entry,
    Frame,
    Label,
    StringVar,
    Widget
)

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


class ConsoleCommandEntry(Frame):
    '''
        Interactive command input bar providing prompt, text entry, and dispatch button.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _on_send - Dispatched command callback.
                | _entry_var - Tkinter StringVar holding current input text.
                | _lbl_prompt - Prompt Label component.
                | _entry_cmd - Text Entry input box.
                | _btn_send - Send Button component.
            :methods:
                | __init__ - Builds prompt, input entry, and send button.
                | get_command - Returns current command string.
                | clear_command - Clears input field.
                | _handle_send - Validates input and dispatches command.
    '''

    DEFAULT_STYLE: Final[ConsolePanelStyle] = ConsolePanelStyle()

    _on_send: Callable[[str], None]
    _entry_var: StringVar
    _lbl_prompt: Label
    _entry_cmd: Entry
    _btn_send: Button

    def __init__(
        self,
        parent: Widget,
        on_send: Callable[[str], None],
        style: ConsolePanelStyle | None = None
    ) -> None:
        '''
            Initializes command entry bar.

            :param parent: Parent Tkinter widget.
            :param on_send: Callback invoked when command is submitted.
            :param style: Optional visual styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        cfg: ConsolePanelStyle = style or self.DEFAULT_STYLE
        self._on_send = on_send
        self._entry_var = StringVar()

        self._lbl_prompt = Label(
            self,
            text=cfg.prompt_text,
            font=(ThemeManager.FONT_MONO, cfg.prompt_font_size),
            fg=ThemeManager.ACCENT_CYAN,
            bg=ThemeManager.BG_PANEL
        )
        self._lbl_prompt.pack(side=LEFT, padx=cfg.prompt_pad_x)

        self._entry_cmd = Entry(
            self,
            textvariable=self._entry_var,
            font=(ThemeManager.FONT_MONO, cfg.entry_font_size),
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT
        )
        self._entry_cmd.pack(side=LEFT, fill=X, expand=True, padx=cfg.entry_pad_x)
        self._entry_cmd.bind('<Return>', lambda _e: self._handle_send())

        self._btn_send = Button(
            self,
            text=cfg.btn_send_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_send_font_size, 'bold'),
            bg=ThemeManager.ACCENT_CYAN,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=cfg.btn_send_pad_x,
            pady=cfg.btn_send_pad_y,
            command=self._handle_send
        )
        self._btn_send.pack(side=RIGHT)

    def get_command(self) -> str:
        '''
            Reads currently entered command string.

            :return: Stripped command text.
        '''
        return self._entry_var.get().strip()

    def clear_command(self) -> None:
        '''
            Clears input field.
        '''
        self._entry_var.set('')

    def _handle_send(self) -> None:
        '''
            Validates command string and fires dispatch callback.
        '''
        cmd: str = self.get_command()
        if cmd:
            self._on_send(cmd)
            self.clear_command()
