# -*- coding: UTF-8 -*-

'''
Module
    console_panel_style.py
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
    Visual style and layout metrics configuration for serial console panel.
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
class ConsolePanelStyle:
    '''
        Visual styling, dimensions, and text labels for command console.

        It defines:

            :attributes:
                | panel_pad_x - Horizontal inner padding for console panel.
                | panel_pad_y - Vertical inner padding for console panel.
                | header_pad_bottom - Vertical spacing below console header.
                | cmd_entry_pad_top - Vertical spacing above command entry row.
                | title_text - Section title label string.
                | title_font_size - Section title font size in points.
                | btn_clear_text - Label string for Clear action button.
                | btn_copy_text - Label string for Copy action button.
                | btn_select_all_text - Label string for Select All action button.
                | action_btn_font_size - Font size in points for header buttons.
                | action_btn_pad_x - Horizontal inner padding for header buttons.
                | action_btn_pad_y - Vertical inner padding for header buttons.
                | action_btn_spacing_x - Horizontal margin tuple for header buttons.
                | prompt_text - Indicator prompt string.
                | prompt_font_size - Font size in points for prompt label.
                | prompt_pad_x - Margin tuple after prompt label.
                | entry_font_size - Font size in points for command entry text.
                | entry_pad_x - Margin tuple after command entry text field.
                | btn_send_text - Label string for Send command button.
                | btn_send_font_size - Font size in points for Send button.
                | btn_send_pad_x - Inner horizontal padding for Send button.
                | btn_send_pad_y - Inner vertical padding for Send button.
                | default_log_height - Default visible text lines in log viewer.
                | log_font_size - Monospace font size in points for log text.
                | log_pad_x - Inner horizontal padding for text viewer area.
                | log_pad_y - Inner vertical padding for text viewer area.
                | arrow_tx - Arrow indicator for transmitted messages.
                | arrow_rx - Arrow indicator for received messages.
                | err_prefix - Error prefix string identifying warning lines.
                | text_wrap_mode - Tkinter text wrap mode string.
                | text_state_disabled - Text widget disabled state string.
                | text_state_normal - Text widget normal state string.
                | start_index - Beginning index string for text buffer.
                | dir_tx - Transmitted message direction identifier.
                | key_ctrl_a_lower - Lowercase select all shortcut key sequence.
                | key_ctrl_a_upper - Uppercase select all shortcut key sequence.
                | key_ctrl_c_lower - Lowercase copy shortcut key sequence.
                | key_ctrl_c_upper - Uppercase copy shortcut key sequence.
                | timestamp_template - Format template for serial log timestamps.
    '''

    panel_pad_x: int = 10
    panel_pad_y: int = 8
    header_pad_bottom: int = 6
    cmd_entry_pad_top: int = 6

    title_text: str = 'SERIAL MONITOR & COMMAND CONSOLE'
    title_font_size: int = 9

    btn_clear_text: str = 'Clear'
    btn_copy_text: str = 'Copy'
    btn_select_all_text: str = 'Select All'
    action_btn_font_size: int = 8
    action_btn_pad_x: int = 8
    action_btn_pad_y: int = 1
    action_btn_spacing_x: tuple[int, int] = (0, 6)

    prompt_text: str = 'cmd >'
    prompt_font_size: int = 9
    prompt_pad_x: tuple[int, int] = (0, 6)

    entry_font_size: int = 9
    entry_pad_x: tuple[int, int] = (0, 6)

    btn_send_text: str = 'Send'
    btn_send_font_size: int = 9
    btn_send_pad_x: int = 12
    btn_send_pad_y: int = 2

    default_log_height: int = 7
    log_font_size: int = 9
    log_pad_x: int = 6
    log_pad_y: int = 6
    arrow_tx: str = '-> '
    arrow_rx: str = '<- '
    err_prefix: str = 'ERR'

    text_wrap_mode: str = 'none'
    text_state_disabled: str = 'disabled'
    text_state_normal: str = 'normal'
    start_index: str = '1.0'
    dir_tx: str = 'TX'
    key_ctrl_a_lower: str = '<Control-a>'
    key_ctrl_a_upper: str = '<Control-A>'
    key_ctrl_c_lower: str = '<Control-c>'
    key_ctrl_c_upper: str = '<Control-C>'
    timestamp_template: str = '[{timestamp}] '
