# -*- coding: UTF-8 -*-

'''
Module
    preset_panel.py
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
    Toolbar container for quickly selecting and triggering posture presets.
'''

from __future__ import annotations

from tkinter import (
    FLAT,
    LEFT,
    TOP,
    X,
    Button,
    Frame,
    Label,
    Widget
)
from typing import Callable

from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PresetPanel(Frame):
    '''
        Toolbar displaying available motion presets as actionable buttons.

        It defines:

            :attributes:
                | _presets - Sequence of MotionPreset objects.
                | _on_apply_preset - Callback invoked when a preset button is clicked.
            :methods:
                | __init__ - Builds preset button row.
    '''

    _presets: tuple[MotionPreset, ...]
    _on_apply_preset: Callable[[MotionPreset], None]

    def __init__(
        self,
        parent: Widget,
        presets: tuple[MotionPreset, ...],
        on_apply_preset: Callable[[MotionPreset], None]
    ) -> None:
        '''
            Initializes preset toolbar.

            :param parent: Parent container.
            :param presets: Predefined motion presets.
            :param on_apply_preset: Callback handler.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL, padx=12, pady=6)
        self._presets = presets
        self._on_apply_preset = on_apply_preset

        lbl_title = Label(
            self,
            text='POSTURE PRESETS:',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_PANEL
        )
        lbl_title.pack(side=LEFT, padx=(0, 10))

        for preset in self._presets:
            btn = Button(
                self,
                text=preset.name,
                font=(ThemeManager.FONT_FAMILY, 8),
                bg=ThemeManager.BG_CARD,
                fg=ThemeManager.ACCENT_CYAN,
                relief=FLAT,
                padx=10,
                pady=3,
                command=lambda p=preset: self._on_apply_preset(p)
            )
            btn.pack(side=LEFT, padx=(0, 6))
