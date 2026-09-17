# -*- coding: UTF-8 -*-

'''
Module
    mecha_console_view.py
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
    Diagnostic console view for displaying Mecha DSL syntax and compilation feedback.
'''

from __future__ import annotations

from tkinter import BOTH, END, RIGHT, VERTICAL, Widget, Y, Text, Frame, Scrollbar
from typing import Any

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaConsoleView(Frame):
    '''
        Diagnostic console panel presenting linter feedback and compilation output.

        It defines:

            :attributes:
                | _txt_console - Internal multi-line read-only Text widget.
            :methods:
                | __init__ - Configures console layout and visual tags.
                | append_message - Appends formatted message string to output.
                | show_diagnostics - Renders tuple of diagnostic items.
                | clear - Clears all console messages.
    '''

    _txt_console: Text

    def __init__(self, parent: Widget, height: int = 6, **kwargs: object) -> None:
        '''
            Configures console widget layout and styles.

            :param parent: Parent container widget.
            :param height: Text height in lines.
        '''
        super().__init__(parent, bg=ThemeManager.BG_DARK, **kwargs)

        scroll_y = Scrollbar(self, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self._txt_console = Text(
            self,
            height=height,
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 9),
            wrap='word',
            yscrollcommand=scroll_y.set,
            bd=0,
            padx=6,
            pady=4
        )
        self._txt_console.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self._txt_console.yview)

        self._txt_console.tag_configure('error', foreground=ThemeManager.ACCENT_RED)
        self._txt_console.tag_configure('warning', foreground=ThemeManager.ACCENT_ORANGE)
        self._txt_console.tag_configure('info', foreground=ThemeManager.TEXT_PRIMARY)
        self._txt_console.tag_configure('success', foreground=ThemeManager.ACCENT_GREEN)

    def append_message(self, text: str, tag: str = 'info') -> None:
        '''
            Appends a message to the console output.

            :param text: Text string to append.
            :param tag: Color formatting tag ('error', 'warning', 'info', 'success').
        '''
        self._txt_console.insert(END, text + '\n', tag)
        self._txt_console.see(END)

    def show_diagnostics(self, diagnostics: tuple[Any, ...]) -> None:
        '''
            Renders diagnostic items into the console.

            :param diagnostics: Tuple of MechaDiagnostic instances.
        '''
        self.clear()
        if not diagnostics:
            self.append_message('✅ Code validated successfully: No errors or warnings found.', 'success')
            return

        for diag in diagnostics:
            tag = 'error' if diag.severity.value == 'ERROR' else 'warning'
            self.append_message(diag.formatted_message(), tag)

    def clear(self) -> None:
        '''Clears all messages from console buffer.'''
        self._txt_console.delete('1.0', END)
