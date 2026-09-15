# -*- coding: UTF-8 -*-

'''
Module
    joint_control_widget.py
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
    Individual joint slider and precision stepping controller widget.
'''

from __future__ import annotations

from tkinter import (
    HORIZONTAL,
    LEFT,
    RIGHT,
    TOP,
    X,
    DoubleVar,
    Frame,
    Label,
    Scale,
    Widget
)
from typing import Callable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.kinematics.joint_state import JointState
from mecharmory.infrastructure.gui.theme import ThemeManager
from mecharmory.infrastructure.gui.joint.joint_step_buttons import (
    JointStepButtons
)
from mecharmory.infrastructure.gui.joint.joint_entry_control import (
    JointEntryControl
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointControlWidget(Frame):
    '''
        Interactive widget providing slider, fine stepping buttons, and direct angle input.

        It defines:

            :attributes:
                | _config - Static JointConfig parameters.
                | _state - Dynamic JointState model reference.
                | _on_angle_change - Callback dispatched when new angle is set.
                | _slider_var - Tkinter DoubleVar for scale slider.
                | _lbl_current - Label showing real-time feedback position.
                | _slider - Horizontal Scale slider.
                | _entry_ctrl - Direct entry and set button component.
            :methods:
                | __init__ - Builds widget hierarchy and binds events.
                | update_display - Refreshes visual labels to match model state.
                | _on_slider_moved - Handles user dragging the slider.
                | _step_angle - Adjusts angle by fixed delta (+/- 1 or 5 deg).
                | _on_entry_apply - Applies manually typed angle from entry box.
    '''

    _config: JointConfig
    _state: JointState
    _on_angle_change: Callable[[JointId, float], None]
    _slider_var: DoubleVar
    _lbl_current: Label
    _slider: Scale
    _entry_ctrl: JointEntryControl

    def __init__(
        self,
        parent: Widget,
        config: JointConfig,
        state: JointState,
        on_angle_change: Callable[[JointId, float], None]
    ) -> None:
        '''
            Initializes joint widget.

            :param parent: Parent Tkinter container.
            :param config: Joint configuration.
            :param state: Joint state.
            :param on_angle_change: Dispatched angle change handler.
        '''
        super().__init__(
            parent,
            bg=ThemeManager.BG_CARD,
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground=ThemeManager.BORDER_COLOR
        )
        self._config = config
        self._state = state
        self._on_angle_change = on_angle_change
        self._slider_var = DoubleVar(value=state.target_angle)

        # Header Frame
        header = Frame(self, bg=ThemeManager.BG_CARD)
        header.pack(fill=X, side=TOP, pady=(0, 4))

        lbl_name = Label(
            header,
            text=f'{self._config.name}',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            fg=ThemeManager.ACCENT_CYAN,
            bg=ThemeManager.BG_CARD
        )
        lbl_name.pack(side=LEFT)

        lbl_range = Label(
            header,
            text=f' [{self._config.min_deg:.0f}° - {self._config.max_deg:.0f}°]',
            font=(ThemeManager.FONT_FAMILY, 8),
            fg=ThemeManager.TEXT_SECONDARY,
            bg=ThemeManager.BG_CARD
        )
        lbl_range.pack(side=LEFT)

        self._lbl_current = Label(
            header,
            text=f'Pos: {self._state.current_angle:.1f}°',
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            fg=ThemeManager.ACCENT_GREEN,
            bg=ThemeManager.BG_CARD
        )
        self._lbl_current.pack(side=RIGHT)

        # Controls Row
        ctrl = Frame(self, bg=ThemeManager.BG_CARD)
        ctrl.pack(fill=X, side=TOP)

        JointStepButtons.pack_negative_buttons(ctrl, self._step_angle)

        self._slider = Scale(
            ctrl,
            from_=self._config.min_deg,
            to=self._config.max_deg,
            resolution=0.5,
            orient=HORIZONTAL,
            variable=self._slider_var,
            bg=ThemeManager.BG_CARD,
            fg=ThemeManager.TEXT_PRIMARY,
            troughcolor=ThemeManager.BG_DARK,
            activebackground=ThemeManager.ACCENT_CYAN,
            highlightthickness=0,
            showvalue=False,
            command=self._on_slider_moved
        )
        self._slider.pack(side=LEFT, fill=X, expand=True, padx=4)

        JointStepButtons.pack_positive_buttons(ctrl, self._step_angle)

        self._entry_ctrl = JointEntryControl(
            ctrl,
            on_apply=self._on_entry_apply,
            initial_val=state.target_angle
        )
        self._entry_ctrl.pack(side=LEFT)

    def update_display(self) -> None:
        '''
            Updates real-time positions from model.
        '''
        self._lbl_current.config(
            text=f'Pos: {self._state.current_angle:.1f}°',
            fg=ThemeManager.ACCENT_YELLOW if self._state.is_moving else ThemeManager.ACCENT_GREEN
        )
        if abs(self._slider_var.get() - self._state.target_angle) > 0.4:
            self._slider_var.set(self._state.target_angle)
            self._entry_ctrl.set_value(self._state.target_angle)

    def _on_slider_moved(self, val_str: str) -> None:
        '''
            Dispatches slider movement.

            :param val_str: Scale value string.
        '''
        try:
            val: float = float(val_str)
            self._entry_ctrl.set_value(val)
            self._on_angle_change(self._config.joint_id, val)
        except ValueError:
            pass

    def _step_angle(self, delta: float) -> None:
        '''
            Steps angle by offset.

            :param delta: Angle offset.
        '''
        new_val: float = self._slider_var.get() + delta
        if new_val < self._config.min_deg:
            new_val = self._config.min_deg
        if new_val > self._config.max_deg:
            new_val = self._config.max_deg

        self._slider_var.set(new_val)
        self._entry_ctrl.set_value(new_val)
        self._on_angle_change(self._config.joint_id, new_val)

    def _on_entry_apply(self, val: float) -> None:
        '''
            Applies angle typed directly in entry.

            :param val: Numeric value.
        '''
        if val < self._config.min_deg:
            val = self._config.min_deg
        if val > self._config.max_deg:
            val = self._config.max_deg

        self._slider_var.set(val)
        self._entry_ctrl.set_value(val)
        self._on_angle_change(self._config.joint_id, val)
