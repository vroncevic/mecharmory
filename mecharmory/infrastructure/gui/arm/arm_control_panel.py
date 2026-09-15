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
    Panel grouping all 6 joint control widgets and global motion action buttons.
'''

from __future__ import annotations

from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    TOP,
    X,
    Button,
    Frame,
    Label,
    Widget
)
from typing import Callable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme import ThemeManager
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


class ArmControlPanel(Frame):
    '''
        Panel managing all 6 joint sliders and global emergency stop / home actions.

        It defines:

            :attributes:
                | _model - IArmModel interface.
                | _joint_widgets - Mapping of JointId to JointControlWidget.
                | _on_joint_command - Dispatched angle change handler.
                | _on_home - Dispatched home action.
                | _on_stop - Dispatched emergency stop action.
                | _on_status - Dispatched query status action.
            :methods:
                | __init__ - Builds header toolbar and 6 joint control rows.
                | refresh_telemetry - Calls update_display on each child joint widget.
    '''

    _model: IArmModel
    _joint_widgets: dict[JointId, JointControlWidget]
    _on_joint_command: Callable[[JointId, float], None]
    _on_home: Callable[[], None]
    _on_stop: Callable[[], None]
    _on_status: Callable[[], None]

    def __init__(
        self,
        parent: Widget,
        model: IArmModel,
        on_joint_command: Callable[[JointId, float], None],
        on_home: Callable[[], None],
        on_stop: Callable[[], None],
        on_status: Callable[[], None]
    ) -> None:
        '''
            Initializes arm control panel.

            :param parent: Parent container.
            :param model: Domain ArmModel.
            :param on_joint_command: Joint angle change callback.
            :param on_home: Home action callback.
            :param on_stop: Stop action callback.
            :param on_status: Query status callback.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL, padx=12, pady=10)
        self._model = model
        self._on_joint_command = on_joint_command
        self._on_home = on_home
        self._on_stop = on_stop
        self._on_status = on_status
        self._joint_widgets = {}

        # Header with Global Actions
        header = Frame(self, bg=ThemeManager.BG_PANEL)
        header.pack(fill=X, side=TOP, pady=(0, 10))

        lbl_section = Label(
            header,
            text='JOINT CONTROLS',
            font=(ThemeManager.FONT_FAMILY, 10, 'bold'),
            fg=ThemeManager.TEXT_PRIMARY,
            bg=ThemeManager.BG_PANEL
        )
        lbl_section.pack(side=LEFT)

        # Stop Button (Right)
        btn_stop = Button(
            header,
            text='EMERGENCY STOP',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            bg=ThemeManager.ACCENT_RED,
            fg='#ffffff',
            relief=FLAT,
            padx=10,
            pady=3,
            command=self._on_stop
        )
        btn_stop.pack(side=RIGHT, padx=(6, 0))

        # Home Button
        btn_home = Button(
            header,
            text='Home All',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            bg=ThemeManager.ACCENT_BLUE,
            fg=ThemeManager.BG_DARK,
            relief=FLAT,
            padx=10,
            pady=3,
            command=self._on_home
        )
        btn_home.pack(side=RIGHT, padx=(6, 0))

        # Query Status Button
        btn_query = Button(
            header,
            text='Query Status',
            font=(ThemeManager.FONT_FAMILY, 8),
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_PRIMARY,
            relief=FLAT,
            padx=8,
            pady=3,
            command=self._on_status
        )
        btn_query.pack(side=RIGHT)

        # Create widgets for all 6 joints
        for jid in (
            JointId.BASE,
            JointId.LIFT_1,
            JointId.LIFT_2,
            JointId.TUBE_ROLL,
            JointId.END_PITCH,
            JointId.TOOL_ROLL
        ):
            cfg = self._model.get_config(jid)
            st = self._model.get_state(jid)
            widget = JointControlWidget(
                self,
                config=cfg,
                state=st,
                on_angle_change=self._on_joint_command
            )
            widget.pack(fill=X, side=TOP, pady=3)
            self._joint_widgets[jid] = widget

    def refresh_telemetry(self) -> None:
        '''Updates visual displays across all joint subwidgets.'''
        for widget in self._joint_widgets.values():
            widget.update_display()
