# -*- coding: UTF-8 -*-

'''
Module
    arm_panel_style.py
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
    Visual style, metrics, and labels configuration for arm control panel.
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
class ArmPanelStyle:
    '''
        Visual styling, dimensions, and text labels for arm control panel.

        It defines:

            :attributes:
                | panel_pad_x - Horizontal inner padding for arm control panel.
                | panel_pad_y - Vertical inner padding for arm control panel.
                | header_pad_bottom - Vertical spacing below header toolbar in pixels.
                | title_text - Section title label string.
                | title_font_size - Section title font size in points.
                | title_font_weight - Section title font weight.
                | btn_font_weight - Action buttons font weight.
                | btn_stop_text - Emergency stop button text.
                | btn_stop_font_size - Emergency stop button font size in points.
                | btn_stop_fg - Emergency stop text foreground color.
                | btn_stop_pad_x - Emergency stop button horizontal inner padding.
                | btn_stop_pad_y - Emergency stop button vertical inner padding.
                | btn_home_text - Home all axes button text.
                | btn_home_font_size - Home all axes button font size in points.
                | btn_home_pad_x - Home all axes button horizontal inner padding.
                | btn_home_pad_y - Home all axes button vertical inner padding.
                | btn_query_text - Query status button text.
                | btn_query_font_size - Query status button font size in points.
                | btn_query_pad_x - Query status button horizontal inner padding.
                | btn_query_pad_y - Query status button vertical inner padding.
                | btn_spacing_x - Horizontal margin tuple between action buttons.
                | joint_widget_pad_y - Vertical spacing between joint control widgets.
    '''

    panel_pad_x: int = 12
    panel_pad_y: int = 10
    header_pad_bottom: int = 10

    title_text: str = 'JOINT CONTROLS'
    title_font_size: int = 10
    title_font_weight: str = 'bold'

    btn_font_weight: str = 'bold'
    btn_stop_text: str = 'EMERGENCY STOP'
    btn_stop_font_size: int = 9
    btn_stop_fg: str = '#ffffff'
    btn_stop_pad_x: int = 10
    btn_stop_pad_y: int = 3

    btn_home_text: str = 'Home All'
    btn_home_font_size: int = 9
    btn_home_pad_x: int = 10
    btn_home_pad_y: int = 3

    btn_query_text: str = 'Query Status'
    btn_query_font_size: int = 8
    btn_query_pad_x: int = 8
    btn_query_pad_y: int = 3

    btn_spacing_x: tuple[int, int] = (6, 0)
    joint_widget_pad_y: int = 3
