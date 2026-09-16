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


class JointStepButtons:
    '''
        Constructs and binds negative and positive fine-stepping angle adjustment buttons.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
            :methods:
                | pack_negative_buttons - Builds -5 deg and -1 deg step buttons.
                | pack_positive_buttons - Builds +1 deg and +5 deg step buttons.
    '''

    DEFAULT_STYLE: JointWidgetStyle = JointWidgetStyle()

    @classmethod
    def pack_negative_buttons(
        cls,
        parent: Widget,
        on_step: Callable[[float], None],
        style: JointWidgetStyle | None = None
    ) -> None:
        '''
            Packs negative stepping buttons into control container.

            :param parent: Parent container widget.
            :param on_step: Callback invoked with delta angle.
            :param style: Optional visual styling configuration.
        '''
        cfg: JointWidgetStyle = style or cls.DEFAULT_STYLE
        btn_m5 = Button(
            parent,
            text=cfg.btn_m5_text,
            width=cfg.step_btn_width,
            font=(ThemeManager.FONT_FAMILY, cfg.step_btn_font_size),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            pady=cfg.step_btn_pad_y,
            command=lambda: on_step(-cfg.step_delta_large)
        )
        btn_m5.pack(side=LEFT, padx=cfg.step_m5_pad_x)

        btn_m1 = Button(
            parent,
            text=cfg.btn_m1_text,
            width=cfg.step_btn_width,
            font=(ThemeManager.FONT_FAMILY, cfg.step_btn_font_size),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            pady=cfg.step_btn_pad_y,
            command=lambda: on_step(-cfg.step_delta_small)
        )
        btn_m1.pack(side=LEFT, padx=cfg.step_m1_pad_x)

    @classmethod
    def pack_positive_buttons(
        cls,
        parent: Widget,
        on_step: Callable[[float], None],
        style: JointWidgetStyle | None = None
    ) -> None:
        '''
            Packs positive stepping buttons into control container.

            :param parent: Parent container widget.
            :param on_step: Callback invoked with delta angle.
            :param style: Optional visual styling configuration.
        '''
        cfg: JointWidgetStyle = style or cls.DEFAULT_STYLE
        btn_p1 = Button(
            parent,
            text=cfg.btn_p1_text,
            width=cfg.step_btn_width,
            font=(ThemeManager.FONT_FAMILY, cfg.step_btn_font_size),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            pady=cfg.step_btn_pad_y,
            command=lambda: on_step(cfg.step_delta_small)
        )
        btn_p1.pack(side=LEFT, padx=cfg.step_p1_pad_x)

        btn_p5 = Button(
            parent,
            text=cfg.btn_p5_text,
            width=cfg.step_btn_width,
            font=(ThemeManager.FONT_FAMILY, cfg.step_btn_font_size),
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            pady=cfg.step_btn_pad_y,
            command=lambda: on_step(cfg.step_delta_large)
        )
        btn_p5.pack(side=LEFT, padx=cfg.step_p5_pad_x)
