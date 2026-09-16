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

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.joint.joint_widget_style import (
    JointWidgetStyle
)

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
                | DEFAULT_STYLE - Default visual styling parameters.
                | _on_apply - Callback invoked with verified angle.
                | _entry_var - Tkinter StringVar holding input text.
                | _entry - Tkinter Entry box.
                | _btn_set - Set submission button.
                | _style - Visual styling configuration reference.
            :methods:
                | __init__ - Configures entry field, set button, and Return key binding.
                | set_value - Updates visual text without dispatching.
                | get_value - Reads current text string.
                | _apply - Parses number and dispatches apply callback.
    '''

    DEFAULT_STYLE: JointWidgetStyle = JointWidgetStyle()

    _on_apply: Callable[[float], None]
    _entry_var: StringVar
    _entry: Entry
    _btn_set: Button
    _style: JointWidgetStyle

    def __init__(
        self,
        parent: Widget,
        on_apply: Callable[[float], None],
        initial_val: float,
        style: JointWidgetStyle | None = None
    ) -> None:
        '''
            Initializes entry control widgets.

            :param parent: Parent container.
            :param on_apply: Callback invoked on angle entry.
            :param initial_val: Starting numeric value.
            :param style: Optional visual styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_CARD)
        cfg: JointWidgetStyle = style or self.DEFAULT_STYLE
        self._style = cfg
        self._on_apply = on_apply
        self._entry_var = StringVar(value=cfg.entry_val_template.format(val=initial_val))

        self._entry = Entry(
            self,
            textvariable=self._entry_var,
            width=cfg.entry_width,
            font=(ThemeManager.FONT_MONO, cfg.entry_font_size),
            bg=ThemeManager.BG_DARK,
            fg=ThemeManager.TEXT_PRIMARY,
            insertbackground=ThemeManager.TEXT_PRIMARY,
            relief=FLAT
        )
        self._entry.pack(side=LEFT, padx=cfg.entry_pad_x)
        self._entry.bind('<Return>', lambda e: self._apply())

        self._btn_set = Button(
            self,
            text=cfg.btn_set_text,
            font=(ThemeManager.FONT_FAMILY, cfg.btn_set_font_size, 'bold'),
            bg=ThemeManager.ACCENT_BLUE,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=cfg.btn_set_pad_x,
            pady=cfg.btn_set_pad_y,
            command=self._apply
        )
        self._btn_set.pack(side=LEFT)

    def set_value(self, val: float) -> None:
        '''
            Sets entry display text.

            :param val: Angle float.
        '''
        self._entry_var.set(self._style.entry_val_template.format(val=val))

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
