# -*- coding: UTF-8 -*-

'''
Module
    gui_window_style.py
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
    Visual style, dimensions, and timing metrics for main GUI application window.
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
class GuiWindowStyle:
    '''
        Visual styling, dimensions, and timing metrics for master application window.

        It defines:

            :attributes:
                | window_title - Main application window title text.
                | window_geometry - Fixed dimensions string of main window.
                | poll_interval_ms - Periodic UI update polling frequency in milliseconds.
                | protocol_delete_window - Tkinter window deletion protocol name.
                | body_pad_x - Horizontal padding for main body frame.
                | body_pad_y - Vertical padding for main body frame.
                | upper_row_spacing_y - Vertical padding margin for upper workspace row.
                | left_col_spacing_x - Horizontal padding margin for left column.
                | control_panel_spacing_y - Vertical padding margin for control panel.
                | right_col_width - Fixed pixel width for right kinematics preview column.
    '''

    window_title: str = 'Mecharmory - 6-DOF Robotic Arm Studio'
    window_geometry: str = '1280x920'
    poll_interval_ms: int = 100
    protocol_delete_window: str = 'WM_DELETE_WINDOW'
    body_pad_x: int = 10
    body_pad_y: int = 8
    upper_row_spacing_y: tuple[int, int] = (0, 8)
    left_col_spacing_x: tuple[int, int] = (0, 8)
    control_panel_spacing_y: tuple[int, int] = (0, 8)
    right_col_width: int = 480
