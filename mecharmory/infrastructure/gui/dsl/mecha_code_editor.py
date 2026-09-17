# -*- coding: UTF-8 -*-

'''
Module
    mecha_code_editor.py
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
    Syntax-highlighted multi-line code editor component for Mecha DSL scripts.
'''

from __future__ import annotations

from tkinter import BOTH, END, Event, Misc, RIGHT, VERTICAL, Widget, Y, Text, Frame, Scrollbar

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.dsl.mecha_syntax_highlighter import (
    MechaSyntaxHighlighter,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaCodeEditor(Frame):
    '''
        Scrolled multi-line text editor with syntax highlighting and undo/redo support.

        It defines:

            :attributes:
                | _txt_editor - Inner multi-line Text widget.
                | _highlighter - Syntax highlighter instance.
            :methods:
                | __init__ - Initializes the editor container and binds syntax highlighter.
                | get_text - Returns full contents of the editor buffer.
                | set_text - Replaces editor buffer with provided text.
                | clear - Clears all text in the editor.
                | highlight - Triggers manual syntax highlighting refresh.
    '''

    _txt_editor: Text
    _highlighter: MechaSyntaxHighlighter

    def __init__(self, parent: Widget, **kwargs: object) -> None:
        '''
            Initializes editor container and binds syntax highlighter.

            :param parent: Parent container widget.
        '''
        super().__init__(parent, bg=ThemeManager.BG_DARK, **kwargs)

        scroll_y = Scrollbar(self, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self._txt_editor = Text(
            self,
            width=1,
            bg=ThemeManager.BG_CANVAS,
            fg=ThemeManager.TEXT_PRIMARY,
            insertbackground=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 10),
            wrap='none',
            yscrollcommand=scroll_y.set,
            undo=True,
            bd=0,
            padx=8,
            pady=8
        )
        self._txt_editor.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self._txt_editor.yview)

        self._highlighter = MechaSyntaxHighlighter(self._txt_editor)
        self._txt_editor.bind('<KeyRelease>', self._on_key_release)

    def _on_key_release(self, _event: Event[Misc]) -> None:
        '''Refreshes syntax highlighting on keystrokes.'''
        self._highlighter.highlight(self._txt_editor)

    def get_text(self) -> str:
        '''
            Returns entire contents of text editor buffer.

            :return: String code content.
        '''
        return self._txt_editor.get('1.0', END).rstrip()

    def set_text(self, text: str) -> None:
        '''
            Replaces buffer content with provided text.

            :param text: New script source code.
        '''
        self._txt_editor.delete('1.0', END)
        self._txt_editor.insert('1.0', text)
        self._highlighter.highlight(self._txt_editor)

    def clear(self) -> None:
        '''Clears all text from editor.'''
        self._txt_editor.delete('1.0', END)

    def highlight(self) -> None:
        '''Triggers manual refresh of syntax colors.'''
        self._highlighter.highlight(self._txt_editor)
