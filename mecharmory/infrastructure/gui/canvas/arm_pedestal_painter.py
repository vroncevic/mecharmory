# -*- coding: UTF-8 -*-

'''
Module
    arm_pedestal_painter.py
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
    Base pedestal and yaw turntable indicator painter for 2D arm canvas.
'''

from __future__ import annotations

from math import cos, sin, radians
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


class ArmPedestalPainter:
    '''
        Renders robotic arm base pedestal and yaw turntable indicator.

        It defines:

            :methods:
                | paint - Draws pedestal and yaw turntable on canvas.
    '''

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        x0: float,
        ground_y: float,
        y_sh: float,
        yaw_deg: float,
        style: ArmCanvasStyle
    ) -> None:
        '''
            Draws base pedestal and yaw turntable indicator.

            :param canvas: Target Tkinter canvas.
            :param x0: Center X coordinate.
            :param ground_y: Ground level Y.
            :param y_sh: Shoulder height Y.
            :param yaw_deg: Yaw rotation in degrees.
            :param style: Visual styling configuration.
        '''
        canvas.create_rectangle(
            x0 - style.pedestal_half_width,
            ground_y,
            x0 + style.pedestal_half_width,
            y_sh,
            fill=ThemeManager.BG_CARD,
            outline=ThemeManager.BORDER_COLOR,
            width=style.pedestal_outline_width
        )
        yaw_rad: float = radians(yaw_deg)
        ptr_x: float = x0 + style.turntable_radius_x * cos(yaw_rad)
        ptr_y: float = (ground_y + y_sh) * 0.5 - style.turntable_radius_y * sin(yaw_rad)
        canvas.create_oval(
            x0 - style.turntable_radius_x,
            (ground_y + y_sh) * 0.5 - style.turntable_radius_y,
            x0 + style.turntable_radius_x,
            (ground_y + y_sh) * 0.5 + style.turntable_radius_y,
            outline=ThemeManager.ACCENT_BLUE,
            width=style.turntable_outline_width
        )
        canvas.create_line(
            x0,
            (ground_y + y_sh) * 0.5,
            ptr_x,
            ptr_y,
            fill=ThemeManager.ACCENT_CYAN,
            width=style.turntable_arrow_width,
            arrow=style.turntable_arrow_style
        )
