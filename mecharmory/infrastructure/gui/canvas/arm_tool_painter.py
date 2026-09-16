# -*- coding: UTF-8 -*-

'''
Module
    arm_tool_painter.py
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
    Wrist joint, end bracket, and tool flange painter for 2D arm canvas.
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


class ArmToolPainter:
    '''
        Renders wrist joint, end tilt bracket, tool flange, and tool roll marker.

        It defines:

            :methods:
                | paint - Draws wrist joint, tilt bracket, flange, and roll mark.
    '''

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        x_wr: float,
        y_wr: float,
        x_tl: float,
        y_tl: float,
        rad_end: float,
        tool_deg: float,
        style: ArmCanvasStyle
    ) -> None:
        '''
            Draws end bracket tilt link and rotating tool flange.

            :param canvas: Target Tkinter canvas.
            :param x_wr: Wrist pivot X coordinate.
            :param y_wr: Wrist pivot Y coordinate.
            :param x_tl: Tool center X coordinate.
            :param y_tl: Tool center Y coordinate.
            :param rad_end: End effector pitch angle in radians.
            :param tool_deg: Tool roll in degrees.
            :param style: Visual styling configuration.
        '''
        r: float = style.wrist_joint_radius
        canvas.create_oval(
            x_wr - r,
            y_wr - r,
            x_wr + r,
            y_wr + r,
            fill=ThemeManager.ACCENT_YELLOW,
            outline=style.joint_outline_color,
            width=style.joint_outline_width
        )
        canvas.create_line(
            x_wr,
            y_wr,
            x_tl,
            y_tl,
            fill=ThemeManager.ACCENT_ORANGE,
            width=style.wrist_link_width,
            capstyle='round'
        )

        perp: float = rad_end + radians(90.0)
        tool_r: float = style.tool_flange_radius
        tx1: float = x_tl + tool_r * cos(perp)
        ty1: float = y_tl - tool_r * sin(perp)
        tx2: float = x_tl - tool_r * cos(perp)
        ty2: float = y_tl + tool_r * sin(perp)
        canvas.create_line(
            tx1,
            ty1,
            tx2,
            ty2,
            fill=ThemeManager.ACCENT_GREEN,
            width=style.tool_flange_width
        )

        mark_len: float = style.tool_mark_length * cos(radians(tool_deg))
        mx: float = x_tl + mark_len * cos(rad_end)
        my: float = y_tl - mark_len * sin(rad_end)
        canvas.create_line(
            x_tl,
            y_tl,
            mx,
            my,
            fill=style.tool_mark_color,
            width=style.tool_mark_width
        )
