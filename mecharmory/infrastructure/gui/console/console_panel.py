# -*- coding: UTF-8 -*-

'''
Module
    console_panel.py
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
    Interactive serial log monitor and manual command console.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    END,
    FLAT,
    LEFT,
    RIGHT,
    TOP,
    X,
    Y,
    Button,
    Entry,
    Frame,
    Label,
    Scrollbar,
    StringVar,
    Text,
    Widget
)
from typing import Callable

from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConsolePanel(Frame):
    '''
        Displays real-time communication messages and provides manual command injection.

        It defines:

            :attributes:
                | _on_send - Callback when manual command is submitted.
                | _text_area - Scrollable Text widget.
                | _entry_var - Tkinter StringVar for input line.
            :methods:
                | __init__ - Configures text viewer, scrollbar, and input bar.
                | append_message - Formats and displays a SerialMessage.
                | clear_log - Empties console content.
                | _handle_send - Dispatches input text.
    '''

    _on_send: Callable[[str], None]
    _text_area: Text
    _entry_var: StringVar

    def __init__(self, parent: Widget, on_send: Callable[[str], None]) -> None:
        '''
            Initializes console panel.

            :param parent: Parent Tkinter widget.
            :param on_send: Command submit callback.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL, padx=10, pady=8)
        self._on_send = on_send
        self._entry_var = StringVar()

        # Header
        header = Frame(self, bg=ThemeManager.BG_PANEL)
        header.pack(fill=X, side=TOP, pady=(0, 6))

        lbl_title = Label(
            header,
            text='SERIAL MONITOR & COMMAND CONSOLE',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        lbl_title.pack(side=LEFT)

        btn_clear = Button(
            header,
            text='Clear',
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_SECONDARY,
            relief=FLAT,
            padx=8,
            pady=1,
            command=self.clear_log
        )
        btn_clear.pack(side=RIGHT)

        # Log Area Frame
        log_frame = Frame(self, bg=ThemeManager.BG_DARK)
        log_frame.pack(fill=BOTH, expand=True, side=TOP)

        scrollbar = Scrollbar(log_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._text_area = Text(
            log_frame,
            wrap='none',
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_MONO, 9),
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=6,
            pady=6,
            yscrollcommand=scrollbar.set,
            state='disabled'
        )
        self._text_area.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self._text_area.yview)

        # Text color tags
        self._text_area.tag_config('tx', foreground=ThemeManager.ACCENT_CYAN)
        self._text_area.tag_config('rx', foreground=ThemeManager.ACCENT_GREEN)
        self._text_area.tag_config('timestamp', foreground=ThemeManager.TEXT_SECONDARY)
        self._text_area.tag_config('error', foreground=ThemeManager.ACCENT_RED)

        # Command Entry Row
        cmd_frame = Frame(self, bg=ThemeManager.BG_PANEL)
        cmd_frame.pack(fill=X, side=TOP, pady=(6, 0))

        lbl_prompt = Label(
            cmd_frame,
            text='cmd >',
            font=(ThemeManager.FONT_MONO, 9),
            fg=ThemeManager.ACCENT_CYAN,
            bg=ThemeManager.BG_PANEL
        )
        lbl_prompt.pack(side=LEFT, padx=(0, 6))

        entry_cmd = Entry(
            cmd_frame,
            textvariable=self._entry_var,
            font=(ThemeManager.FONT_MONO, 9),
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT
        )
        entry_cmd.pack(side=LEFT, fill=X, expand=True, padx=(0, 6))
        entry_cmd.bind('<Return>', lambda e: self._handle_send())

        btn_send = Button(
            cmd_frame,
            text='Send',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            bg=ThemeManager.ACCENT_CYAN,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=12,
            pady=2,
            command=self._handle_send
        )
        btn_send.pack(side=RIGHT)

    def append_message(self, message: SerialMessage) -> None:
        '''
            Appends formatted message to console buffer and scrolls to end.

            :param message: SerialMessage domain instance.
        '''
        self._text_area.config(state='normal')
        self._text_area.insert(END, f'[{message.timestamp}] ', 'timestamp')

        if message.direction == 'TX':
            self._text_area.insert(END, '-> ', 'tx')
            self._text_area.insert(END, f'{message.text}\n')
        else:
            self._text_area.insert(END, '<- ', 'rx')
            tag: str = 'error' if message.text.startswith('ERR') else 'rx'
            self._text_area.insert(END, f'{message.text}\n', tag)

        self._text_area.see(END)
        self._text_area.config(state='disabled')

    def clear_log(self) -> None:
        '''
            Clears text monitor buffer.
        '''
        self._text_area.config(state='normal')
        self._text_area.delete('1.0', END)
        self._text_area.config(state='disabled')

    def _handle_send(self) -> None:
        '''
            Dispatches typed command and clears input entry.
        '''
        cmd: str = self._entry_var.get().strip()
        if cmd:
            self._on_send(cmd)
            self._entry_var.set('')
