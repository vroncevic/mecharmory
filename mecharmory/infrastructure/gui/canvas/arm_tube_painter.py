# -*- coding: UTF-8 -*-

'''
Module
    arm_tube_painter.py
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
    Elbow joint and cylindrical forearm tube painter for 2D arm canvas.
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


class ArmTubePainter:
    '''
        Renders elbow pivot joint, forearm tube casing, and axial roll indicator.

        It defines:

            :methods:
                | paint - Draws elbow joint, tube layers, and roll indicator on canvas.
    '''

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        x_el: float,
        y_el: float,
        x_wr: float,
        y_wr: float,
        rad_tube: float,
        roll_deg: float,
        style: ArmCanvasStyle
    ) -> None:
        '''
            Draws circular tube and axial rotation roll indicator.

            :param canvas: Target Tkinter canvas.
            :param x_el: Elbow pivot X coordinate.
            :param y_el: Elbow pivot Y coordinate.
            :param x_wr: Wrist pivot X coordinate.
            :param y_wr: Wrist pivot Y coordinate.
            :param rad_tube: Forearm tube angle in radians.
            :param roll_deg: Forearm roll angle in degrees.
            :param style: Visual styling configuration.
        '''
        r: float = style.elbow_joint_radius
        canvas.create_oval(
            x_el - r,
            y_el - r,
            x_el + r,
            y_el + r,
            fill=ThemeManager.ACCENT_CYAN,
            outline=style.joint_outline_color,
            width=style.joint_outline_width
        )
        canvas.create_line(
            x_el,
            y_el,
            x_wr,
            y_wr,
            fill=style.tube_base_color,
            width=style.tube_outer_width,
            capstyle=style.tube_cap_style
        )
        canvas.create_line(
            x_el,
            y_el,
            x_wr,
            y_wr,
            fill=style.tube_inner_color,
            width=style.tube_inner_width,
            capstyle=style.tube_cap_style
        )

        mid_x: float = (x_el + x_wr) * 0.5
        mid_y: float = (y_el + y_wr) * 0.5
        perp: float = rad_tube + radians(90.0)
        roll_span: float = style.roll_indicator_span * sin(radians(roll_deg))
        rx: float = roll_span * cos(perp)
        ry: float = roll_span * sin(perp)
        canvas.create_line(
            mid_x - rx,
            mid_y - ry,
            mid_x + rx,
            mid_y + ry,
            fill=ThemeManager.ACCENT_YELLOW,
            width=style.roll_indicator_width
        )
