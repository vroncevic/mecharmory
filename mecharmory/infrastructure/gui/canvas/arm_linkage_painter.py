# -*- coding: UTF-8 -*-

'''
Module
    arm_linkage_painter.py
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
    Dual lift mechanism and boom linkage painter for 2D arm canvas.
'''

from __future__ import annotations

from math import cos, sin
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


class ArmLinkagePainter:
    '''
        Renders shoulder joint, main lifting boom, and parallel linkage rod.

        It defines:

            :methods:
                | paint - Draws boom link and parallel rod on canvas.
    '''

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        x_sh: float,
        y_sh: float,
        x_el: float,
        y_el: float,
        rad_boom: float,
        style: ArmCanvasStyle
    ) -> None:
        '''
            Draws main lifting boom and parallel linkage rod.

            :param canvas: Target Tkinter canvas.
            :param x_sh: Shoulder pivot X coordinate.
            :param y_sh: Shoulder pivot Y coordinate.
            :param x_el: Elbow pivot X coordinate.
            :param y_el: Elbow pivot Y coordinate.
            :param rad_boom: Boom angle in radians.
            :param style: Visual styling configuration.
        '''
        ox: float = style.rod_offset * sin(rad_boom)
        oy: float = style.rod_offset * cos(rad_boom)
        canvas.create_line(
            x_sh - ox,
            y_sh - oy,
            x_el - ox,
            y_el - oy,
            fill=ThemeManager.BORDER_COLOR,
            width=style.rod_line_width,
            dash=style.rod_dash_pattern
        )
        canvas.create_line(
            x_sh,
            y_sh,
            x_el,
            y_el,
            fill=ThemeManager.ACCENT_BLUE,
            width=style.boom_line_width,
            capstyle=style.boom_cap_style
        )
        r: float = style.shoulder_joint_radius
        canvas.create_oval(
            x_sh - r,
            y_sh - r,
            x_sh + r,
            y_sh + r,
            fill=ThemeManager.ACCENT_BLUE,
            outline=style.joint_outline_color,
            width=style.joint_outline_width
        )
