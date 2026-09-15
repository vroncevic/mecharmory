# -*- coding: UTF-8 -*-

'''
Module
    arm_canvas_painter.py
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
    Visual renderer drawing robotic arm linkages and telemetry onto a Tkinter Canvas.
'''

from __future__ import annotations

from math import cos, sin, radians
from tkinter import Canvas

from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.gui.canvas.arm_pose_2d import ArmPose2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmCanvasPainter:
    '''
        Renders 2D graphical schematics for robotic arm manipulator segments.

        It defines:

            :methods:
                | paint - Clears and paints complete arm posture and HUD overlay.
                | draw_background - Renders ground line and label.
                | draw_base_pedestal - Renders base pedestal and yaw turntable.
                | draw_dual_lift_mechanism - Renders boom link and linkage rod.
                | draw_cylindrical_tube - Renders elbow tube and roll indicator.
                | draw_end_and_tool - Renders wrist link and tool flange.
                | draw_hud - Renders HUD telemetry text.
    '''

    @classmethod
    def paint(cls, canvas: Canvas, pose: ArmPose2D, w: int, ground_y: float) -> None:
        '''
            Paints all schematic components according to computed pose.

            :param canvas: Target Tkinter drawing surface.
            :param pose: Computed 2D pose coordinates.
            :param w: Width of canvas.
            :param ground_y: Ground plane Y coordinate.
            :exceptions: None.
        '''
        canvas.delete('all')
        cls.draw_background(canvas, w, ground_y)
        cls.draw_base_pedestal(canvas, pose.x0, ground_y, pose.y_sh, pose.angles[0])
        cls.draw_dual_lift_mechanism(canvas, pose.x0, pose.y_sh, pose.x_el, pose.y_el, pose.rad_boom)
        cls.draw_cylindrical_tube(canvas, pose.x_el, pose.y_el, pose.x_wr, pose.y_wr, pose.rad_tube, pose.angles[3])
        cls.draw_end_and_tool(canvas, pose.x_wr, pose.y_wr, pose.x_tl, pose.y_tl, pose.rad_end, pose.angles[5])
        cls.draw_hud(canvas, w, pose.angles)

    @classmethod
    def draw_background(cls, canvas: Canvas, w: int, ground_y: float) -> None:
        '''
            Draws ground plane.

            :param canvas: Target canvas.
            :param w: Canvas width.
            :param ground_y: Ground coordinate.
        '''
        canvas.create_line(12, ground_y, w - 12, ground_y, fill=ThemeManager.BORDER_COLOR, width=2)
        canvas.create_text(
            22, ground_y + 12,
            text='GROUND',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 7)
        )

    @classmethod
    def draw_base_pedestal(
        cls,
        canvas: Canvas,
        x0: float,
        ground_y: float,
        y_sh: float,
        yaw_deg: float
    ) -> None:
        '''
            Draws base pedestal and yaw turntable indicator.

            :param canvas: Target canvas.
            :param x0: Center X coordinate.
            :param ground_y: Ground level Y.
            :param y_sh: Shoulder height Y.
            :param yaw_deg: Yaw rotation in degrees.
        '''
        canvas.create_rectangle(
            x0 - 26, ground_y, x0 + 26, y_sh,
            fill=ThemeManager.BG_CARD, outline=ThemeManager.BORDER_COLOR, width=2
        )
        yaw_rad: float = radians(yaw_deg)
        ptr_x: float = x0 + 18.0 * cos(yaw_rad)
        ptr_y: float = (ground_y + y_sh) * 0.5 - 6.0 * sin(yaw_rad)
        canvas.create_oval(
            x0 - 18, (ground_y + y_sh) * 0.5 - 6,
            x0 + 18, (ground_y + y_sh) * 0.5 + 6,
            outline=ThemeManager.ACCENT_BLUE, width=1
        )
        canvas.create_line(
            x0, (ground_y + y_sh) * 0.5, ptr_x, ptr_y,
            fill=ThemeManager.ACCENT_CYAN, width=2, arrow='last'
        )

    @classmethod
    def draw_dual_lift_mechanism(
        cls,
        canvas: Canvas,
        x_sh: float,
        y_sh: float,
        x_el: float,
        y_el: float,
        rad_boom: float
    ) -> None:
        '''
            Draws main lifting boom and parallel linkage rod.

            :param canvas: Target canvas.
            :param x_sh: Shoulder X.
            :param y_sh: Shoulder Y.
            :param x_el: Elbow X.
            :param y_el: Elbow Y.
            :param rad_boom: Boom angle in radians.
        '''
        ox: float = 9.0 * sin(rad_boom)
        oy: float = 9.0 * cos(rad_boom)
        canvas.create_line(
            x_sh - ox, y_sh - oy, x_el - ox, y_el - oy,
            fill=ThemeManager.BORDER_COLOR, width=3, dash=(4, 2)
        )
        canvas.create_line(
            x_sh, y_sh, x_el, y_el,
            fill=ThemeManager.ACCENT_BLUE, width=7, capstyle='round'
        )
        canvas.create_oval(
            x_sh - 6, y_sh - 6, x_sh + 6, y_sh + 6,
            fill=ThemeManager.ACCENT_BLUE, outline='#ffffff', width=1.5
        )

    @classmethod
    def draw_cylindrical_tube(
        cls,
        canvas: Canvas,
        x_el: float,
        y_el: float,
        x_wr: float,
        y_wr: float,
        rad_tube: float,
        roll_deg: float
    ) -> None:
        '''
            Draws circular tube and axial rotation roll indicator.

            :param canvas: Target canvas.
            :param x_el: Elbow X.
            :param y_el: Elbow Y.
            :param x_wr: Wrist X.
            :param y_wr: Wrist Y.
            :param rad_tube: Tube angle in radians.
            :param roll_deg: Roll angle in degrees.
        '''
        canvas.create_oval(
            x_el - 7, y_el - 7, x_el + 7, y_el + 7,
            fill=ThemeManager.ACCENT_CYAN, outline='#ffffff', width=1.5
        )
        canvas.create_line(x_el, y_el, x_wr, y_wr, fill='#9399b2', width=8, capstyle='round')
        canvas.create_line(x_el, y_el, x_wr, y_wr, fill='#cdd6f4', width=3, capstyle='round')

        mid_x: float = (x_el + x_wr) * 0.5
        mid_y: float = (y_el + y_wr) * 0.5
        perp: float = rad_tube + radians(90.0)
        roll_span: float = 7.0 * sin(radians(roll_deg))
        rx: float = roll_span * cos(perp)
        ry: float = roll_span * sin(perp)
        canvas.create_line(
            mid_x - rx, mid_y - ry, mid_x + rx, mid_y + ry,
            fill=ThemeManager.ACCENT_YELLOW, width=3
        )

    @classmethod
    def draw_end_and_tool(
        cls,
        canvas: Canvas,
        x_wr: float,
        y_wr: float,
        x_tl: float,
        y_tl: float,
        rad_end: float,
        tool_deg: float
    ) -> None:
        '''
            Draws end bracket tilt link and rotating tool flange.

            :param canvas: Target canvas.
            :param x_wr: Wrist X.
            :param y_wr: Wrist Y.
            :param x_tl: Tool X.
            :param y_tl: Tool Y.
            :param rad_end: End angle in radians.
            :param tool_deg: Tool roll in degrees.
        '''
        canvas.create_oval(
            x_wr - 5, y_wr - 5, x_wr + 5, y_wr + 5,
            fill=ThemeManager.ACCENT_YELLOW, outline='#ffffff', width=1.5
        )
        canvas.create_line(x_wr, y_wr, x_tl, y_tl, fill=ThemeManager.ACCENT_ORANGE, width=5, capstyle='round')

        perp: float = rad_end + radians(90.0)
        tool_r: float = 12.0
        tx1: float = x_tl + tool_r * cos(perp)
        ty1: float = y_tl - tool_r * sin(perp)
        tx2: float = x_tl - tool_r * cos(perp)
        ty2: float = y_tl + tool_r * sin(perp)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=ThemeManager.ACCENT_GREEN, width=4)

        mark_len: float = 6.0 * cos(radians(tool_deg))
        mx: float = x_tl + mark_len * cos(rad_end)
        my: float = y_tl - mark_len * sin(rad_end)
        canvas.create_line(x_tl, y_tl, mx, my, fill='#ffffff', width=2)

    @classmethod
    def draw_hud(
        cls,
        canvas: Canvas,
        w: int,
        angles: tuple[float, float, float, float, float, float]
    ) -> None:
        '''
            Renders HUD state text overlay.

            :param canvas: Target canvas.
            :param w: Canvas width.
            :param angles: Joint angles tuple.
        '''
        txt: str = (
            f'J0 Yaw: {angles[0]:.0f}° | J1 Lift: {angles[1]:.0f}°\n'
            f'J2 Rod: {angles[2]:.0f}° | J3 Tube: {angles[3]:.0f}°\n'
            f'J4 End: {angles[4]:.0f}° | J5 Tool: {angles[5]:.0f}°'
        )
        canvas.create_text(
            w - 10, 12,
            anchor='ne',
            text=txt,
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 8),
            justify='right'
        )
