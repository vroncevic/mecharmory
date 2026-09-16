# -*- coding: UTF-8 -*-

'''
Module
    console_log_viewer.py
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
    Scrollable text viewer displaying serial message communication history.
'''

from __future__ import annotations

from typing import Final

from tkinter import (
    BOTH,
    END,
    FLAT,
    LEFT,
    RIGHT,
    Y,
    Frame,
    Scrollbar,
    Text,
    Widget
)

from mecharmory.core.model.communication.serial_message import SerialMessage
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


class ConsoleLogViewer(Frame):
    '''
        Scrollable log display with syntax highlighting, selection, and clipboard support.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | TAG_TX - Tag identifier for transmitted messages.
                | TAG_RX - Tag identifier for received messages.
                | TAG_TIMESTAMP - Tag identifier for timestamp prefixes.
                | TAG_ERROR - Tag identifier for error messages.
                | _text_area - Primary Tkinter Text display surface.
                | _scrollbar - Vertical Scrollbar component.
                | _style - Visual styling configuration reference.
            :methods:
                | __init__ - Configures text viewer, scrollbar, tags, and shortcuts.
                | append_message - Formats and appends a SerialMessage.
                | clear - Empties console log content.
                | select_all - Highlights entire text buffer.
                | copy_to_clipboard - Copies selected text or complete buffer to clipboard.
    '''

    DEFAULT_STYLE: Final[ConsolePanelStyle] = ConsolePanelStyle()
    TAG_TX: Final[str] = 'tx'
    TAG_RX: Final[str] = 'rx'
    TAG_TIMESTAMP: Final[str] = 'timestamp'
    TAG_ERROR: Final[str] = 'error'

    _text_area: Text
    _scrollbar: Scrollbar
    _style: ConsolePanelStyle

    def __init__(
        self,
        parent: Widget,
        height: int | None = None,
        style: ConsolePanelStyle | None = None
    ) -> None:
        '''
            Initializes console log viewer.

            :param parent: Parent Tkinter widget.
            :param height: Optional visible line height of the text area.
            :param style: Optional visual styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_DARK)
        cfg: ConsolePanelStyle = style or self.DEFAULT_STYLE
        self._style = cfg
        lines_height: int = height if height is not None else cfg.default_log_height

        self._scrollbar = Scrollbar(self)
        self._scrollbar.pack(side=RIGHT, fill=Y)

        self._text_area = Text(
            self,
            height=lines_height,
            wrap=cfg.text_wrap_mode,
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_MONO, cfg.log_font_size),
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=cfg.log_pad_x,
            pady=cfg.log_pad_y,
            yscrollcommand=self._scrollbar.set,
            state=cfg.text_state_disabled
        )
        self._text_area.pack(side=LEFT, fill=BOTH, expand=True)
        self._scrollbar.config(command=self._text_area.yview)

        self._text_area.bind(cfg.key_ctrl_a_lower, self.select_all)
        self._text_area.bind(cfg.key_ctrl_a_upper, self.select_all)
        self._text_area.bind(cfg.key_ctrl_c_lower, self.copy_to_clipboard)
        self._text_area.bind(cfg.key_ctrl_c_upper, self.copy_to_clipboard)

        self._text_area.tag_config(self.TAG_TX, foreground=ThemeManager.ACCENT_CYAN)
        self._text_area.tag_config(self.TAG_RX, foreground=ThemeManager.ACCENT_GREEN)
        self._text_area.tag_config(self.TAG_TIMESTAMP, foreground=ThemeManager.TEXT_SECONDARY)
        self._text_area.tag_config(self.TAG_ERROR, foreground=ThemeManager.ACCENT_RED)

    def append_message(self, message: SerialMessage) -> None:
        '''
            Appends formatted message to console buffer and scrolls to end.

            :param message: SerialMessage domain instance.
        '''
        self._text_area.config(state=self._style.text_state_normal)
        ts_str: str = self._style.timestamp_template.format(timestamp=message.timestamp)
        self._text_area.insert(END, ts_str, self.TAG_TIMESTAMP)

        if message.direction == self._style.dir_tx:
            self._text_area.insert(END, self._style.arrow_tx, self.TAG_TX)
            self._text_area.insert(END, f'{message.text}\n')
        else:
            self._text_area.insert(END, self._style.arrow_rx, self.TAG_RX)
            tag: str = self.TAG_ERROR if message.text.startswith(self._style.err_prefix) else self.TAG_RX
            self._text_area.insert(END, f'{message.text}\n', tag)

        self._text_area.see(END)
        self._text_area.config(state=self._style.text_state_disabled)

    def clear(self) -> None:
        '''
            Clears all log lines in buffer.
        '''
        self._text_area.config(state=self._style.text_state_normal)
        self._text_area.delete(self._style.start_index, END)
        self._text_area.config(state=self._style.text_state_disabled)

    def select_all(self, _event: object = None) -> str:
        '''
            Selects all content in the text area buffer.

            :param _event: Optional Tkinter event.
            :return: 'break' to suppress default event handling.
        '''
        self._text_area.tag_add('sel', self._style.start_index, 'end-1c')
        self._text_area.focus_set()

        return 'break'

    def copy_to_clipboard(self, _event: object = None) -> str:
        '''
            Copies selected text or entire log to clipboard.

            :param _event: Optional Tkinter event.
            :return: 'break' to suppress default event handling.
        '''
        try:
            selected_text: str = self._text_area.get('sel.first', 'sel.last')

        except Exception:
            selected_text = self._text_area.get(self._style.start_index, 'end-1c')

        if selected_text:
            self.clipboard_clear()
            self.clipboard_append(selected_text)

        return 'break'
