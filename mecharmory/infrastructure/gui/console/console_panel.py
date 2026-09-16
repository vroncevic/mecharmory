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
    Composite container for serial monitor, action toolbar, and command console.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    BOTTOM,
    TOP,
    X,
    Frame,
    Widget
)
from typing import Callable, Final

from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.console.console_panel_style import (
    ConsolePanelStyle
)
from mecharmory.infrastructure.gui.console.console_header_toolbar import (
    ConsoleHeaderToolbar
)
from mecharmory.infrastructure.gui.console.console_command_entry import (
    ConsoleCommandEntry
)
from mecharmory.infrastructure.gui.console.console_log_viewer import (
    ConsoleLogViewer
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConsolePanel(Frame):
    '''
        Displays real-time communication messages and provides manual command injection.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _header - Header toolbar containing title and action buttons.
                | _cmd_entry - Command prompt and input submission bar.
                | _log_viewer - Scrollable log viewer displaying serial messages.
            :methods:
                | __init__ - Composes toolbar, command bar, and log viewer sub-widgets.
                | append_message - Formats and displays a SerialMessage.
                | clear_log - Empties console content.
                | select_all - Highlights all log content in buffer.
                | copy_to_clipboard - Copies selection or entire log to clipboard.
    '''

    DEFAULT_STYLE: Final[ConsolePanelStyle] = ConsolePanelStyle()

    _header: ConsoleHeaderToolbar
    _cmd_entry: ConsoleCommandEntry
    _log_viewer: ConsoleLogViewer

    def __init__(
        self,
        parent: Widget,
        on_send: Callable[[str], None],
        style: ConsolePanelStyle | None = None
    ) -> None:
        '''
            Initializes composite console panel.

            :param parent: Parent Tkinter widget.
            :param on_send: Command submit callback.
            :param style: Optional visual styling configuration.
        '''
        cfg: ConsolePanelStyle = style or self.DEFAULT_STYLE
        super().__init__(
            parent,
            bg=ThemeManager.BG_PANEL,
            padx=cfg.panel_pad_x,
            pady=cfg.panel_pad_y
        )

        # Header Toolbar (Top)
        self._header = ConsoleHeaderToolbar(
            self,
            on_clear=self.clear_log,
            on_copy=self.copy_to_clipboard,
            on_select_all=self.select_all,
            style=cfg
        )
        self._header.pack(fill=X, side=TOP, pady=(0, cfg.header_pad_bottom))

        # Command Entry Row (Bottom)
        self._cmd_entry = ConsoleCommandEntry(
            self,
            on_send=on_send,
            style=cfg
        )
        self._cmd_entry.pack(fill=X, side=BOTTOM, pady=(cfg.cmd_entry_pad_top, 0))

        # Log Area Viewer (Center - expands between Header and Cmd Entry)
        self._log_viewer = ConsoleLogViewer(self, style=cfg)
        self._log_viewer.pack(fill=BOTH, expand=True, side=TOP)

    def append_message(self, message: SerialMessage) -> None:
        '''
            Appends formatted message to console buffer and scrolls to end.

            :param message: SerialMessage domain instance.
        '''
        self._log_viewer.append_message(message)

    def clear_log(self) -> None:
        '''
            Clears text monitor buffer.
        '''
        self._log_viewer.clear()

    def select_all(self, _event: object | None = None) -> str | None:
        '''
            Selects all content in the text monitor buffer.

            :param _event: Optional Tkinter event.
            :return: 'break' string if invoked via key event.
        '''
        return self._log_viewer.select_all(_event)

    def copy_to_clipboard(self, _event: object | None = None) -> str | None:
        '''
            Copies selected text or complete log buffer to the system clipboard.

            :param _event: Optional Tkinter event.
            :return: 'break' string if invoked via key event.
        '''
        return self._log_viewer.copy_to_clipboard(_event)
