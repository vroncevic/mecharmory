# -*- coding: UTF-8 -*-

'''
Module
    joint_widget_style.py
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
    Visual style and dimension metrics for joint control slider widgets.
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
class JointWidgetStyle:
    '''
        Visual styling, dimensions, and padding for joint control widgets.

        It defines:

            :attributes:
                | card_pad_x - Horizontal inner padding for joint card widget.
                | card_pad_y - Vertical inner padding for joint card widget.
                | card_border_width - Highlight border thickness for joint card.
                | header_pad_bottom - Vertical spacing below joint title row.
                | name_font_size - Font size in points for joint name label.
                | range_font_size - Font size in points for min/max angle range.
                | pos_font_size - Font size in points for current telemetry position.
                | slider_resolution - Smallest increment step for slider widget.
                | slider_pad_x - Horizontal margin around scale slider in pixels.
                | step_btn_width - Character width of fine-stepping buttons.
                | step_btn_font_size - Font size in points for step buttons.
                | step_btn_pad_y - Vertical inner padding for step buttons.
                | btn_m5_text - Text label for -5 deg fine-stepping button.
                | btn_m1_text - Text label for -1 deg fine-stepping button.
                | btn_p1_text - Text label for +1 deg fine-stepping button.
                | btn_p5_text - Text label for +5 deg fine-stepping button.
                | step_delta_large - Angle step delta in degrees for +/-5 buttons.
                | step_delta_small - Angle step delta in degrees for +/-1 buttons.
                | step_m5_pad_x - Horizontal padding tuple for -5 deg button.
                | step_m1_pad_x - Horizontal padding tuple for -1 deg button.
                | step_p1_pad_x - Horizontal padding tuple for +1 deg button.
                | step_p5_pad_x - Horizontal padding tuple for +5 deg button.
                | entry_width - Character width of direct numeric entry field.
                | entry_font_size - Font size in points for entry text.
                | entry_pad_x - Horizontal padding tuple around entry field.
                | entry_val_template - String format template for numeric entry field.
                | btn_set_text - Label string for submission set button.
                | btn_set_font_size - Font size in points for set button.
                | btn_set_pad_x - Horizontal inner padding for set button.
                | btn_set_pad_y - Vertical inner padding for set button.
                | range_template - String format template for min/max angle range.
                | pos_template - String format template for current angle position.
                | sync_threshold_deg - Minimum angle difference triggering slider resync.
    '''

    card_pad_x: int = 10
    card_pad_y: int = 8
    card_border_width: int = 1
    header_pad_bottom: int = 4

    name_font_size: int = 9
    range_font_size: int = 8
    pos_font_size: int = 9

    slider_resolution: float = 0.5
    slider_pad_x: int = 4

    step_btn_width: int = 3
    step_btn_font_size: int = 8
    step_btn_pad_y: int = 1
    btn_m5_text: str = '-5°'
    btn_m1_text: str = '-1°'
    btn_p1_text: str = '+1°'
    btn_p5_text: str = '+5°'
    step_delta_large: float = 5.0
    step_delta_small: float = 1.0
    step_m5_pad_x: tuple[int, int] = (0, 2)
    step_m1_pad_x: tuple[int, int] = (0, 6)
    step_p1_pad_x: tuple[int, int] = (6, 2)
    step_p5_pad_x: tuple[int, int] = (0, 6)

    entry_width: int = 5
    entry_font_size: int = 9
    entry_pad_x: tuple[int, int] = (0, 4)
    entry_val_template: str = '{val:.1f}'

    btn_set_text: str = 'Set'
    btn_set_font_size: int = 8
    btn_set_pad_x: int = 6
    btn_set_pad_y: int = 1

    range_template: str = ' [{min_deg:.0f}° - {max_deg:.0f}°]'
    pos_template: str = 'Pos: {angle:.1f}°'
    sync_threshold_deg: float = 0.4
