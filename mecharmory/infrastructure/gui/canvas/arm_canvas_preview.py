# -*- coding: UTF-8 -*-

'''
Module
    arm_canvas_preview.py
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
    2D schematic visualization canvas showing live robotic arm kinematic posture.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    Canvas,
    Frame,
    Label,
    TOP,
    W,
    Widget
)

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.canvas.arm_kinematics_2d import ArmKinematics2D
from mecharmory.infrastructure.gui.canvas.arm_canvas_painter import ArmCanvasPainter
from mecharmory.infrastructure.gui.canvas.arm_pose_2d import ArmPose2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmCanvasPreview(Frame):
    '''
        Renders real-time 2D kinematic schematic diagram of the robot arm.

        It defines:

            :attributes:
                | TITLE_TEXT - Title header text for preview panel.
                | CANVAS_WIDTH - Default canvas pixel width.
                | CANVAS_HEIGHT - Default canvas pixel height.
                | GROUND_OFFSET - Ground plane pixel offset from bottom.
                | BASE_X0 - Kinematic base pedestal center X coordinate.
                | KINEMATICS_SCALE - Visual link length scaling multiplier.
                | PAD_X - Horizontal container padding in pixels.
                | PAD_Y - Vertical container padding in pixels.
                | PAD_TITLE_Y - Header label vertical padding tuple.
                | TITLE_FONT_SIZE - Header font size in points.
                | TITLE_FONT_WEIGHT - Header font weight.
                | CANVAS_BORDER_WIDTH - Outline highlight thickness for canvas.
                | _model - Reference to IArmModel interface.
                | _canvas - Tkinter drawing surface.
            :methods:
                | __init__ - Configures preview container and canvas.
                | update_pose - Redraws links and joints according to current angles.
    '''

    TITLE_TEXT: str = 'LIVE 2D KINEMATICS PREVIEW'
    CANVAS_WIDTH: int = 460
    CANVAS_HEIGHT: int = 540
    GROUND_OFFSET: float = 55.0
    BASE_X0: float = 110.0
    KINEMATICS_SCALE: float = 1.55
    PAD_X: int = 8
    PAD_Y: int = 8
    PAD_TITLE_Y: tuple[int, int] = (0, 6)
    TITLE_FONT_SIZE: int = 9
    TITLE_FONT_WEIGHT: str = 'bold'
    CANVAS_BORDER_WIDTH: int = 1

    _model: IArmModel
    _canvas: Canvas

    def __init__(self, parent: Widget, model: IArmModel) -> None:
        '''
            Initializes canvas preview.

            :param parent: Parent container.
            :param model: Domain IArmModel interface.
        '''
        super().__init__(
            parent,
            bg=ThemeManager.BG_PANEL,
            padx=self.PAD_X,
            pady=self.PAD_Y
        )
        self._model = model

        lbl_title = Label(
            self,
            text=self.TITLE_TEXT,
            font=(
                ThemeManager.FONT_FAMILY,
                self.TITLE_FONT_SIZE,
                self.TITLE_FONT_WEIGHT
            ),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        lbl_title.pack(side=TOP, anchor=W, pady=self.PAD_TITLE_Y)

        self._canvas = Canvas(
            self,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=ThemeManager.BG_CANVAS,
            highlightthickness=self.CANVAS_BORDER_WIDTH,
            highlightbackground=ThemeManager.BORDER_COLOR
        )
        self._canvas.pack(side=TOP, fill=BOTH, expand=True)
        self.update_pose()

    def update_pose(self) -> None:
        '''
            Redraws arm segments from current angles matching physical kinematics.
        '''
        w: int = self.CANVAS_WIDTH
        h: int = self.CANVAS_HEIGHT
        ground_y: float = float(h - self.GROUND_OFFSET)

        angles: list[float] = [
            self._model.get_state(JointId.BASE).current_angle,
            self._model.get_state(JointId.LIFT_1).current_angle,
            self._model.get_state(JointId.LIFT_2).current_angle,
            self._model.get_state(JointId.TUBE_ROLL).current_angle,
            self._model.get_state(JointId.END_PITCH).current_angle,
            self._model.get_state(JointId.TOOL_ROLL).current_angle
        ]

        pose: ArmPose2D = ArmKinematics2D.compute_pose(
            angles,
            ground_y=ground_y,
            x0=self.BASE_X0,
            scale=self.KINEMATICS_SCALE
        )
        ArmCanvasPainter.paint(self._canvas, pose, w, ground_y)
