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
    Canvas,
    Frame,
    Label,
    TOP,
    Widget
)

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.gui.canvas.arm_kinematics_2d import (
    ArmKinematics2D
)
from mecharmory.infrastructure.gui.canvas.arm_canvas_painter import (
    ArmCanvasPainter
)
from mecharmory.infrastructure.gui.canvas.arm_pose_2d import ArmPose2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmCanvasPreview(Frame):
    '''
        Renders real-time 2D kinematic schematic diagram of the robot arm.

        It defines:

            :attributes:
                | _model - Reference to IArmModel interface.
                | _canvas - Tkinter drawing surface.
            :methods:
                | __init__ - Configures preview container and canvas.
                | update_pose - Redraws links and joints according to current angles.
    '''

    _model: IArmModel
    _canvas: Canvas

    def __init__(self, parent: Widget, model: IArmModel) -> None:
        '''
            Initializes canvas preview.

            :param parent: Parent container.
            :param model: Domain IArmModel interface.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL, padx=8, pady=8)
        self._model = model

        lbl_title = Label(
            self,
            text='LIVE 2D KINEMATICS PREVIEW',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        lbl_title.pack(side=TOP, anchor='w', pady=(0, 6))

        self._canvas = Canvas(
            self,
            width=340,
            height=300,
            bg=ThemeManager.BG_CANVAS,
            highlightthickness=1,
            highlightbackground=ThemeManager.BORDER_COLOR
        )
        self._canvas.pack(side=TOP, fill='both', expand=True)
        self.update_pose()

    def update_pose(self) -> None:
        '''
            Redraws arm segments from current angles matching physical kinematics.
        '''
        w: int = 340
        h: int = 300
        ground_y: float = float(h - 35)

        angles: list[float] = [
            self._model.get_state(JointId.BASE).current_angle,
            self._model.get_state(JointId.LIFT_1).current_angle,
            self._model.get_state(JointId.LIFT_2).current_angle,
            self._model.get_state(JointId.TUBE_ROLL).current_angle,
            self._model.get_state(JointId.END_PITCH).current_angle,
            self._model.get_state(JointId.TOOL_ROLL).current_angle
        ]

        pose: ArmPose2D = ArmKinematics2D.compute_pose(angles, ground_y)
        ArmCanvasPainter.paint(self._canvas, pose, w, ground_y)
