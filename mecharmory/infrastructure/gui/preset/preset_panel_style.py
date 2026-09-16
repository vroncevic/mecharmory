# -*- coding: UTF-8 -*-

'''
Module
    preset_panel_style.py
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
    Visual style and dimension metrics for motion preset selection toolbar.
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
class PresetPanelStyle:
    '''
        Visual styling, dimensions, and padding for preset buttons panel.

        It defines:

            :attributes:
                | panel_pad_x - Horizontal inner padding for preset panel.
                | panel_pad_y - Vertical inner padding for preset panel.
                | title_text - Section title label string.
                | title_font_size - Section title font size in points.
                | title_font_weight - Section title font weight.
                | title_pad_x - Horizontal padding tuple after title label.
                | btn_font_size - Font size in points for preset buttons.
                | btn_pad_x - Horizontal inner padding for preset buttons.
                | btn_pad_y - Vertical inner padding for preset buttons.
                | btn_spacing_x - Horizontal margin tuple after each preset button.
    '''

    panel_pad_x: int = 12
    panel_pad_y: int = 6

    title_text: str = 'POSTURE PRESETS:'
    title_font_size: int = 8
    title_font_weight: str = 'bold'
    title_pad_x: tuple[int, int] = (0, 10)

    btn_font_size: int = 8
    btn_pad_x: int = 10
    btn_pad_y: int = 3
    btn_spacing_x: tuple[int, int] = (0, 6)
