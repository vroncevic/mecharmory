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

from tkinter import Canvas

from mecharmory.infrastructure.gui.canvas.arm_pose_2d import ArmPose2D
from mecharmory.infrastructure.gui.canvas.arm_canvas_style import ArmCanvasStyle
from mecharmory.infrastructure.gui.canvas.arm_background_painter import (
    ArmBackgroundPainter
)
from mecharmory.infrastructure.gui.canvas.arm_pedestal_painter import (
    ArmPedestalPainter
)
from mecharmory.infrastructure.gui.canvas.arm_linkage_painter import (
    ArmLinkagePainter
)
from mecharmory.infrastructure.gui.canvas.arm_tube_painter import ArmTubePainter
from mecharmory.infrastructure.gui.canvas.arm_tool_painter import ArmToolPainter
from mecharmory.infrastructure.gui.canvas.arm_hud_painter import ArmHudPainter

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
        Coordinates visual rendering of robotic arm schematics and telemetry overlay.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling and geometry configuration.
            :methods:
                | paint - Clears and renders complete arm posture and HUD overlay.
                | draw_background - Renders ground reference line and label.
                | draw_base_pedestal - Renders base pedestal and yaw turntable.
                | draw_dual_lift_mechanism - Renders boom link and linkage rod.
                | draw_cylindrical_tube - Renders elbow tube and roll indicator.
                | draw_end_and_tool - Renders wrist link and tool flange.
                | draw_hud - Renders HUD telemetry text overlay.
    '''

    DEFAULT_STYLE: ArmCanvasStyle = ArmCanvasStyle()

    @classmethod
    def paint(
        cls,
        canvas: Canvas,
        pose: ArmPose2D,
        w: int,
        ground_y: float,
        style: ArmCanvasStyle | None = None
    ) -> None:
        '''
            Paints all schematic components according to computed pose.

            :param canvas: Target Tkinter drawing surface.
            :param pose: Computed 2D pose coordinates.
            :param w: Width of canvas in pixels.
            :param ground_y: Ground plane Y coordinate.
            :param style: Optional styling configuration.
        '''
        cfg: ArmCanvasStyle = style or cls.DEFAULT_STYLE
        canvas.delete('all')
        cls.draw_background(canvas, w, ground_y, cfg)
        cls.draw_base_pedestal(
            canvas, pose.x0, ground_y, pose.y_sh, pose.angles[0], cfg
        )
        cls.draw_dual_lift_mechanism(
            canvas, pose.x0, pose.y_sh, pose.x_el, pose.y_el, pose.rad_boom, cfg
        )
        cls.draw_cylindrical_tube(
            canvas, pose.x_el, pose.y_el, pose.x_wr, pose.y_wr,
            pose.rad_tube, pose.angles[3], cfg
        )
        cls.draw_end_and_tool(
            canvas, pose.x_wr, pose.y_wr, pose.x_tl, pose.y_tl,
            pose.rad_end, pose.angles[5], cfg
        )
        cls.draw_hud(canvas, w, pose.angles, cfg)

    @classmethod
    def draw_background(
        cls,
        canvas: Canvas,
        w: int,
        ground_y: float,
        style: ArmCanvasStyle | None = None
    ) -> None:
        '''
            Draws ground reference plane.

            :param canvas: Target canvas.
            :param w: Canvas width in pixels.
            :param ground_y: Ground coordinate.
            :param style: Optional styling configuration.
        '''
        ArmBackgroundPainter.paint(canvas, w, ground_y, style or cls.DEFAULT_STYLE)

    @classmethod
    def draw_base_pedestal(
        cls,
        canvas: Canvas,
        x0: float,
        ground_y: float,
        y_sh: float,
        yaw_deg: float,
        style: ArmCanvasStyle | None = None
    ) -> None:
        '''
            Draws base pedestal and yaw turntable indicator.

            :param canvas: Target canvas.
            :param x0: Center X coordinate.
            :param ground_y: Ground level Y.
            :param y_sh: Shoulder height Y.
            :param yaw_deg: Yaw rotation in degrees.
            :param style: Optional styling configuration.
        '''
        ArmPedestalPainter.paint(
            canvas, x0, ground_y, y_sh, yaw_deg, style or cls.DEFAULT_STYLE
        )

    @classmethod
    def draw_dual_lift_mechanism(
        cls,
        canvas: Canvas,
        x_sh: float,
        y_sh: float,
        x_el: float,
        y_el: float,
        rad_boom: float,
        style: ArmCanvasStyle | None = None
    ) -> None:
        '''
            Draws main lifting boom and parallel linkage rod.

            :param canvas: Target canvas.
            :param x_sh: Shoulder X.
            :param y_sh: Shoulder Y.
            :param x_el: Elbow X.
            :param y_el: Elbow Y.
            :param rad_boom: Boom angle in radians.
            :param style: Optional styling configuration.
        '''
        ArmLinkagePainter.paint(
            canvas, x_sh, y_sh, x_el, y_el, rad_boom, style or cls.DEFAULT_STYLE
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
        roll_deg: float,
        style: ArmCanvasStyle | None = None
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
            :param style: Optional styling configuration.
        '''
        ArmTubePainter.paint(
            canvas, x_el, y_el, x_wr, y_wr, rad_tube, roll_deg,
            style or cls.DEFAULT_STYLE
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
        tool_deg: float,
        style: ArmCanvasStyle | None = None
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
            :param style: Optional styling configuration.
        '''
        ArmToolPainter.paint(
            canvas, x_wr, y_wr, x_tl, y_tl, rad_end, tool_deg,
            style or cls.DEFAULT_STYLE
        )

    @classmethod
    def draw_hud(
        cls,
        canvas: Canvas,
        w: int,
        angles: tuple[float, float, float, float, float, float],
        style: ArmCanvasStyle | None = None
    ) -> None:
        '''
            Renders HUD state text overlay.

            :param canvas: Target canvas.
            :param w: Canvas width.
            :param angles: Joint angles tuple.
            :param style: Optional styling configuration.
        '''
        ArmHudPainter.paint(canvas, w, angles, style or cls.DEFAULT_STYLE)
