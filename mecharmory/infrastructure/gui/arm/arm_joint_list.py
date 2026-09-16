# -*- coding: UTF-8 -*-

'''
Module
    arm_joint_list.py
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
    Container managing layout and telemetry of the 6-DOF joint slider widgets.
'''

from __future__ import annotations

from tkinter import (
    TOP,
    X,
    Frame,
    Widget
)
from typing import Callable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.kinematics.joint_state import JointState
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.arm.arm_panel_style import ArmPanelStyle
from mecharmory.infrastructure.gui.joint.joint_control_widget import (
    JointControlWidget
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmJointList(Frame):
    '''
        Container instantiating and managing the 6 joint slider control widgets.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | ORDERED_JOINTS - Fixed tuple specifying 6-DOF joint iteration order.
                | _model - IArmModel interface.
                | _on_joint_command - Angle dispatch callback.
                | _joint_widgets - Mapping of JointId to JointControlWidget.
            :methods:
                | __init__ - Instantiates and packs 6 joint control widgets.
                | refresh_telemetry - Calls update_display across all joint widgets.
                | get_widget - Retrieves JointControlWidget for given JointId.
    '''

    DEFAULT_STYLE: ArmPanelStyle = ArmPanelStyle()
    ORDERED_JOINTS: tuple[JointId, ...] = (
        JointId.BASE,
        JointId.LIFT_1,
        JointId.LIFT_2,
        JointId.TUBE_ROLL,
        JointId.END_PITCH,
        JointId.TOOL_ROLL
    )

    _model: IArmModel
    _on_joint_command: Callable[[JointId, float], None]
    _joint_widgets: dict[JointId, JointControlWidget]

    def __init__(
        self,
        parent: Widget,
        model: IArmModel,
        on_joint_command: Callable[[JointId, float], None],
        style: ArmPanelStyle | None = None
    ) -> None:
        '''
            Initializes joint slider list.

            :param parent: Parent container widget.
            :param model: Manipulator model interface.
            :param on_joint_command: Angle change callback.
            :param style: Optional styling configuration.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._model = model
        self._on_joint_command = on_joint_command
        self._joint_widgets = {}
        cfg_style: ArmPanelStyle = style or self.DEFAULT_STYLE

        for jid in self.ORDERED_JOINTS:
            cfg: JointConfig = self._model.get_config(jid)
            st: JointState = self._model.get_state(jid)
            widget: JointControlWidget = JointControlWidget(
                self,
                config=cfg,
                state=st,
                on_angle_change=self._on_joint_command
            )
            widget.pack(fill=X, side=TOP, pady=cfg_style.joint_widget_pad_y)
            self._joint_widgets[jid] = widget

    def refresh_telemetry(self) -> None:
        '''
            Updates visual displays across all joint subwidgets.
        '''
        for widget in self._joint_widgets.values():
            widget.update_display()

    def get_widget(self, jid: JointId) -> JointControlWidget | None:
        '''
            Retrieves specific joint control widget by JointId.

            :param jid: Target JointId enum.
            :return: JointControlWidget instance or None.
        '''
        return self._joint_widgets.get(jid)
