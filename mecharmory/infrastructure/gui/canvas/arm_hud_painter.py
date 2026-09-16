# -*- coding: UTF-8 -*-

'''
Module
    arm_hud_painter.py
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
    HUD telemetry text overlay painter for 2D arm canvas.
'''

from __future__ import annotations

from tkinter import Canvas

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.canvas.arm_canvas_style import ArmCanvasStyle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmHudPainter:
    '''
        Renders HUD joint angles telemetry text overlay on canvas.

        It defines:

            :methods:
                | paint - Draws HUD telemetry text overlay on canvas.
    '''

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        w: int,
        angles: tuple[float, float, float, float, float, float],
        style: ArmCanvasStyle
    ) -> None:
        '''
            Renders HUD state text overlay.

            :param canvas: Target Tkinter canvas.
            :param w: Canvas width in pixels.
            :param angles: Joint angles tuple.
            :param style: Visual styling configuration.
        '''
        txt: str = style.hud_template.format(
            angles[0], angles[1], angles[2], angles[3], angles[4], angles[5]
        )
        canvas.create_text(
            w - style.hud_offset_x,
            style.hud_offset_y,
            anchor=style.hud_anchor,
            text=txt,
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, style.hud_font_size),
            justify=style.hud_justify
        )
