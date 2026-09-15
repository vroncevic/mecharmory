# -*- coding: UTF-8 -*-

'''
Module
    joint_step_buttons.py
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
    Fine stepping buttons component for incremental joint angle adjustment.
'''

from __future__ import annotations

from tkinter import FLAT, LEFT, Button, Widget
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


class JointStepButtons:
    '''
        Constructs and binds negative and positive fine-stepping angle adjustment buttons.

        It defines:

            :methods:
                | pack_negative_buttons - Builds -5 deg and -1 deg step buttons.
                | pack_positive_buttons - Builds +1 deg and +5 deg step buttons.
    '''

    @classmethod
    def pack_negative_buttons(
        cls,
        parent: Widget,
        on_step: Callable[[float], None]
    ) -> None:
        '''
            Packs negative stepping buttons into control container.

            :param parent: Parent container widget.
            :param on_step: Callback invoked with delta angle.
            :exceptions: None.
        '''
        btn_m5 = Button(
            parent,
            text='-5°',
            width=3,
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            command=lambda: on_step(-5.0)
        )
        btn_m5.pack(side=LEFT, padx=(0, 2))

        btn_m1 = Button(
            parent,
            text='-1°',
            width=3,
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            command=lambda: on_step(-1.0)
        )
        btn_m1.pack(side=LEFT, padx=(0, 6))

    @classmethod
    def pack_positive_buttons(
        cls,
        parent: Widget,
        on_step: Callable[[float], None]
    ) -> None:
        '''
            Packs positive stepping buttons into control container.

            :param parent: Parent container widget.
            :param on_step: Callback invoked with delta angle.
            :exceptions: None.
        '''
        btn_p1 = Button(
            parent,
            text='+1°',
            width=3,
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            command=lambda: on_step(1.0)
        )
        btn_p1.pack(side=LEFT, padx=(6, 2))

        btn_p5 = Button(
            parent,
            text='+5°',
            width=3,
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            command=lambda: on_step(5.0)
        )
        btn_p5.pack(side=LEFT, padx=(0, 8))
