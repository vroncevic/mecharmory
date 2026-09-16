# -*- coding: UTF-8 -*-

'''
Module
    arm_canvas_style.py
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
    Visual style, metrics, and geometry parameters for arm schematic canvas rendering.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ArmCanvasStyle:
    '''
        Visual styling, geometry metrics, and telemetry format for 2D arm canvas.

        It defines:

            :attributes:
                | ground_text - Ground plane label text.
                | ground_line_padding_x - Horizontal inset for ground line in pixels.
                | ground_line_width - Pixel width of ground reference line.
                | ground_text_x - X coordinate for ground label.
                | ground_text_y_offset - Vertical offset below ground line for label.
                | ground_font_size - Font size in points for ground label.
                | pedestal_half_width - Half width of base pedestal in pixels.
                | pedestal_outline_width - Pedestal rectangle outline width in pixels.
                | turntable_radius_x - Horizontal radius of yaw turntable oval.
                | turntable_radius_y - Vertical radius of yaw turntable oval.
                | turntable_outline_width - Outline width of turntable oval.
                | turntable_arrow_width - Pixel width of yaw turntable direction indicator.
                | turntable_arrow_style - Tkinter arrow head style for yaw line.
                | rod_offset - Perpendicular pixel offset for dual lift linkage rod.
                | rod_line_width - Pixel width of linkage rod line.
                | rod_dash_pattern - Dash pattern tuple for parallel rod.
                | boom_line_width - Pixel width of main lifting boom.
                | boom_cap_style - Cap style for main lifting boom line.
                | shoulder_joint_radius - Shoulder pivot circle radius in pixels.
                | joint_outline_color - Outline color hex for pivot joint markers.
                | joint_outline_width - Outline thickness for pivot joint markers.
                | elbow_joint_radius - Elbow pivot circle radius in pixels.
                | tube_base_color - Outer tube casing color hex.
                | tube_inner_color - Inner tube core color hex.
                | tube_outer_width - Line width of outer tube casing.
                | tube_inner_width - Line width of inner tube core.
                | tube_cap_style - Cap style for cylindrical tube lines.
                | roll_indicator_span - Pixel span multiplier for roll indicator.
                | roll_indicator_width - Line width of tube roll indicator.
                | wrist_joint_radius - Wrist pivot circle radius in pixels.
                | wrist_link_width - Line width of wrist tilt bracket.
                | tool_flange_radius - Half length of tool flange crossbar.
                | tool_flange_width - Line width of tool flange crossbar.
                | tool_mark_length - Length multiplier of tool roll indicator line.
                | tool_mark_color - Color hex of tool roll indicator mark.
                | tool_mark_width - Line width of tool roll indicator mark.
                | hud_offset_x - Inset from right canvas edge for HUD in pixels.
                | hud_offset_y - Inset from top canvas edge for HUD in pixels.
                | hud_anchor - Canvas text anchor for HUD overlay.
                | hud_font_size - Font size in points for HUD overlay.
                | hud_justify - Text justification for HUD overlay.
                | hud_template - Format string template for joint angles telemetry.
    '''

    ground_text: str = 'GROUND'
    ground_line_padding_x: int = 12
    ground_line_width: int = 2
    ground_text_x: int = 42
    ground_text_y_offset: int = 12
    ground_font_size: int = 7

    pedestal_half_width: float = 26.0
    pedestal_outline_width: int = 2
    turntable_radius_x: float = 18.0
    turntable_radius_y: float = 6.0
    turntable_outline_width: int = 1
    turntable_arrow_width: int = 2
    turntable_arrow_style: str = 'last'

    rod_offset: float = 9.0
    rod_line_width: int = 3
    rod_dash_pattern: tuple[int, int] = (4, 2)
    boom_line_width: int = 7
    boom_cap_style: str = 'round'
    shoulder_joint_radius: float = 6.0
    joint_outline_color: str = '#ffffff'
    joint_outline_width: float = 1.5

    elbow_joint_radius: float = 7.0
    tube_base_color: str = '#9399b2'
    tube_inner_color: str = '#cdd6f4'
    tube_outer_width: int = 8
    tube_inner_width: int = 3
    tube_cap_style: str = 'round'
    roll_indicator_span: float = 7.0
    roll_indicator_width: int = 3

    wrist_joint_radius: float = 5.0
    wrist_link_width: int = 5
    tool_flange_radius: float = 12.0
    tool_flange_width: int = 4
    tool_mark_length: float = 6.0
    tool_mark_color: str = '#ffffff'
    tool_mark_width: int = 2

    hud_offset_x: int = 10
    hud_offset_y: int = 12
    hud_anchor: str = 'ne'
    hud_font_size: int = 8
    hud_justify: str = 'right'
    hud_template: str = (
        'J0 Yaw: {0:.0f}° | J1 Lift: {1:.0f}°\n'
        'J2 Rod: {2:.0f}° | J3 Tube: {3:.0f}°\n'
        'J4 End: {4:.0f}° | J5 Tool: {5:.0f}°'
    )
