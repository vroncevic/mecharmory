# -*- coding: UTF-8 -*-

'''
Module
    arm_workspace.py
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
    Two-column composite workspace container for joint controls and kinematics preview.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    LEFT,
    RIGHT,
    TOP,
    X,
    Frame,
    Widget
)

from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.gui_event_mediator import GuiEventMediator
from mecharmory.infrastructure.gui.gui_window_style import GuiWindowStyle
from mecharmory.infrastructure.gui.arm.arm_control_panel import ArmControlPanel
from mecharmory.infrastructure.gui.preset.preset_panel import PresetPanel
from mecharmory.infrastructure.gui.canvas.arm_canvas_preview import (
    ArmCanvasPreview
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmWorkspace(Frame):
    '''
        Composite workspace managing joint controls, preset toolbar, and kinematics preview.

        It defines:

            :attributes:
                | DEFAULT_STYLE - Default visual styling parameters.
                | _control_panel - ArmControlPanel instance.
                | _preset_panel - PresetPanel instance.
                | _canvas_preview - ArmCanvasPreview instance.
            :methods:
                | __init__ - Builds two-column workspace layout.
                | refresh_visuals - Triggers synchronized telemetry and kinematics pose update.
                | get_control_panel - Returns internal ArmControlPanel reference.
                | get_preset_panel - Returns internal PresetPanel reference.
                | get_canvas_preview - Returns internal ArmCanvasPreview reference.
    '''

    DEFAULT_STYLE: GuiWindowStyle = GuiWindowStyle()

    _control_panel: ArmControlPanel
    _preset_panel: PresetPanel
    _canvas_preview: ArmCanvasPreview

    def __init__(
        self,
        parent: Widget,
        model: IArmModel,
        mediator: GuiEventMediator,
        style: GuiWindowStyle | None = None
    ) -> None:
        '''
            Initializes two-column workspace container.

            :param parent: Parent Tkinter widget.
            :param model: Robotic arm domain model interface.
            :param mediator: GUI event mediator coordinating user actions.
            :param style: Optional window layout styling configuration.
        '''
        cfg: GuiWindowStyle = style or self.DEFAULT_STYLE
        super().__init__(parent, bg=ThemeManager.BG_DARK)

        left_col = Frame(self, bg=ThemeManager.BG_DARK)
        left_col.pack(side=LEFT, fill=BOTH, expand=True, padx=cfg.left_col_spacing_x)

        self._control_panel = ArmControlPanel(
            left_col,
            model=model,
            on_joint_command=mediator.on_joint_move,
            on_home=mediator.on_home,
            on_stop=mediator.on_stop,
            on_status=mediator.on_query_status
        )
        self._control_panel.pack(fill=X, side=TOP, pady=cfg.control_panel_spacing_y)

        self._preset_panel = PresetPanel(
            left_col,
            presets=model.get_presets(),
            on_apply_preset=mediator.on_apply_preset
        )
        self._preset_panel.pack(fill=X, side=TOP)

        right_col = Frame(self, bg=ThemeManager.BG_DARK, width=cfg.right_col_width)
        right_col.pack(side=RIGHT, fill=BOTH, expand=False)
        right_col.pack_propagate(False)

        self._canvas_preview = ArmCanvasPreview(right_col, model=model)
        self._canvas_preview.pack(fill=BOTH, expand=True, side=TOP)

    def refresh_visuals(self) -> None:
        '''Updates 2D kinematic arm pose and joint telemetry displays.'''
        self._canvas_preview.update_pose()
        self._control_panel.refresh_telemetry()

    def get_control_panel(self) -> ArmControlPanel:
        '''
            Returns arm control panel reference.

            :return: ArmControlPanel instance.
        '''
        return self._control_panel

    def get_preset_panel(self) -> PresetPanel:
        '''
            Returns preset panel reference.

            :return: PresetPanel instance.
        '''
        return self._preset_panel

    def get_canvas_preview(self) -> ArmCanvasPreview:
        '''
            Returns canvas preview reference.

            :return: ArmCanvasPreview instance.
        '''
        return self._canvas_preview
