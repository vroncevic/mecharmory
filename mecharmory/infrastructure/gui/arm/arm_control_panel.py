# -*- coding: UTF-8 -*-

'''
Module
    arm_control_panel.py
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
    Composite container for robotic arm joint sliders and header action buttons.
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
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.arm.arm_panel_style import ArmPanelStyle
from mecharmory.infrastructure.gui.arm.arm_control_header import ArmControlHeader
from mecharmory.infrastructure.gui.arm.arm_joint_list import ArmJointList

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmControlPanel(Frame):
    '''
        Composite panel managing header actions and joint slider controls.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _header - Header toolbar containing title and global action buttons.
                | _joint_list - Container holding 6 joint slider control widgets.
            :methods:
                | __init__ - Composes header toolbar and joint list sub-widgets.
                | refresh_telemetry - Dispatches display updates across all joint widgets.
    '''

    DEFAULT_STYLE: ArmPanelStyle = ArmPanelStyle()

    _header: ArmControlHeader
    _joint_list: ArmJointList

    def __init__(
        self,
        parent: Widget,
        model: IArmModel,
        on_joint_command: Callable[[JointId, float], None],
        on_home: Callable[[], None],
        on_stop: Callable[[], None],
        on_status: Callable[[], None],
        style: ArmPanelStyle | None = None
    ) -> None:
        '''
            Initializes arm control panel.

            :param parent: Parent container.
            :param model: Domain ArmModel.
            :param on_joint_command: Joint angle change callback.
            :param on_home: Home action callback.
            :param on_stop: Stop action callback.
            :param on_status: Query status callback.
            :param style: Optional styling configuration.
        '''
        cfg: ArmPanelStyle = style or self.DEFAULT_STYLE
        super().__init__(
            parent,
            bg=ThemeManager.BG_PANEL,
            padx=cfg.panel_pad_x,
            pady=cfg.panel_pad_y
        )

        self._header = ArmControlHeader(
            self,
            on_status=on_status,
            on_home=on_home,
            on_stop=on_stop,
            style=cfg
        )
        self._header.pack(fill=X, side=TOP, pady=(0, cfg.header_pad_bottom))

        self._joint_list = ArmJointList(
            self,
            model=model,
            on_joint_command=on_joint_command,
            style=cfg
        )
        self._joint_list.pack(fill=X, side=TOP)

    def refresh_telemetry(self) -> None:
        '''
            Updates visual displays across all joint subwidgets.
        '''
        self._joint_list.refresh_telemetry()
