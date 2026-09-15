# -*- coding: UTF-8 -*-

'''
Module
    joint_entry_control.py
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
    Direct angle numeric entry and validation control widget.
'''

from __future__ import annotations

from tkinter import (
    FLAT,
    LEFT,
    Button,
    Entry,
    Frame,
    StringVar,
    Widget
)
from typing import Callable

from mecharmory.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointEntryControl(Frame):
    '''
        Subpanel providing manual numerical entry and a Set button.

        It defines:

            :attributes:
                | _on_apply - Callback invoked with verified angle.
                | _entry_var - Tkinter StringVar holding input text.
                | _entry - Tkinter Entry box.
                | _btn_set - Set submission button.
            :methods:
                | __init__ - Configures entry field, set button, and Return key binding.
                | set_value - Updates visual text without dispatching.
                | get_value - Reads current text string.
                | _apply - Parses number and dispatches apply callback.
    '''

    _on_apply: Callable[[float], None]
    _entry_var: StringVar
    _entry: Entry
    _btn_set: Button

    def __init__(
        self,
        parent: Widget,
        on_apply: Callable[[float], None],
        initial_val: float
    ) -> None:
        '''
            Initializes entry control widgets.

            :param parent: Parent container.
            :param on_apply: Callback invoked on angle entry.
            :param initial_val: Starting numeric value.
        '''
        super().__init__(parent, bg=ThemeManager.BG_CARD)
        self._on_apply = on_apply
        self._entry_var = StringVar(value=f'{initial_val:.1f}')

        self._entry = Entry(
            self,
            textvariable=self._entry_var,
            width=5,
            font=(ThemeManager.FONT_MONO, 9),
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT
        )
        self._entry.pack(side=LEFT, padx=(0, 4))
        self._entry.bind('<Return>', lambda e: self._apply())

        self._btn_set = Button(
            self,
            text='Set',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            bg=ThemeManager.ACCENT_BLUE,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=6,
            command=self._apply
        )
        self._btn_set.pack(side=LEFT)

    def set_value(self, val: float) -> None:
        '''
            Sets entry display text.

            :param val: Angle float.
        '''
        self._entry_var.set(f'{val:.1f}')

    def get_value(self) -> str:
        '''
            Returns current entry text.

            :return: String value.
        '''
        return self._entry_var.get()

    def _apply(self) -> None:
        '''
            Validates and dispatches numerical input.
        '''
        try:
            val: float = float(self._entry_var.get())
            self._on_apply(val)
        except ValueError:
            pass
