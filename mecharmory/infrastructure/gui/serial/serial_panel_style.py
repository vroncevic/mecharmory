# -*- coding: UTF-8 -*-

'''
Module
    serial_panel_style.py
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
    Visual style and layout metrics configuration for serial communication bar.
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
class SerialPanelStyle:
    '''
        Visual styling, dimensions, and padding for serial toolbar and subwidgets.

        It defines:

            :attributes:
                | bar_height - Fixed pixel height of top connection bar.
                | bar_pad_x - Horizontal inner padding for serial bar.
                | bar_pad_y - Vertical inner padding for serial bar.
                | title_text - Brand / application title string.
                | title_font_size - Font size in points for brand title.
                | title_pad_x - Horizontal padding tuple after brand title.
                | port_label_text - Port selector label string.
                | port_combo_width - Character width of port selection combobox.
                | btn_scan_text - Label string for port scanning button.
                | btn_scan_pad_x - Inner padding for scan button.
                | baud_label_text - Baudrate selector label string.
                | baud_combo_width - Character width of baudrate combobox.
                | baudrates - Supported baudrate choices tuple.
                | default_baud - Default selected baudrate.
                | btn_connect_text - Action text for connecting.
                | btn_disconnect_text - Action text for disconnecting.
                | status_offline_text - Status badge text when disconnected.
                | badge_font_size - Font size in points for badge and connect button.
                | badge_pad_x - Inner horizontal padding for connect button.
                | badge_pad_y - Inner vertical padding for connect button.
                | virtual_mode_text - Label text for virtual firmware checkbutton.
                | virtual_font_size - Font size in points for virtual mode label.
                | virtual_pad_x - Horizontal margin tuple for virtual checkbutton.
                | btn_ping_text - Ping button label text.
                | btn_ping_font_size - Font size in points for ping button.
                | btn_ping_pad_x - Inner horizontal padding for ping button.
                | btn_ping_pad_y - Inner vertical padding for ping button.
                | connect_btn_spacing_x - Horizontal spacing tuple after connect button.
                | label_font_size - Font size in points for port and baud labels.
                | label_pad_x - Horizontal padding tuple after field labels.
                | combo_pad_x - Horizontal padding tuple after port combobox.
                | combo_state - Combobox state literal.
                | btn_scan_font_size - Font size in points for scan button.
                | btn_scan_pad_y - Vertical inner padding for scan button.
                | btn_scan_spacing_x - Horizontal margin tuple after scan button.
                | baud_combo_spacing_x - Horizontal margin tuple after baud combobox.
                | fallback_ports - Default port choices when scanner detects none.
                | btn_disconnect_fg - Text foreground color for disconnect button.
                | status_disconnected_text - Status label text when disconnected.
    '''

    bar_height: int = 44
    bar_pad_x: int = 12
    bar_pad_y: int = 6

    title_text: str = 'Mecharmo 6-DOF'
    title_font_size: int = 11
    title_pad_x: tuple[int, int] = (0, 15)

    port_label_text: str = 'Port:'
    port_combo_width: int = 15
    btn_scan_text: str = 'Scan'
    btn_scan_pad_x: int = 8
    btn_scan_pad_y: int = 2
    btn_scan_font_size: int = 8
    btn_scan_spacing_x: tuple[int, int] = (0, 12)

    label_font_size: int = 9
    label_pad_x: tuple[int, int] = (0, 4)
    combo_pad_x: tuple[int, int] = (0, 6)
    combo_state: str = 'readonly'
    fallback_ports: tuple[str, ...] = ('/dev/ttyACM0', '/dev/ttyUSB0')

    baud_label_text: str = 'Baud:'
    baud_combo_width: int = 8
    baud_combo_spacing_x: tuple[int, int] = (0, 12)
    baudrates: tuple[int, ...] = (9600, 19200, 38400, 57600, 115200)
    default_baud: int = 115200

    btn_connect_text: str = 'Connect'
    btn_disconnect_text: str = 'Disconnect'
    btn_disconnect_fg: str = '#ffffff'
    connect_btn_spacing_x: tuple[int, int] = (0, 12)
    status_offline_text: str = 'Offline'
    status_disconnected_text: str = 'Disconnected'
    badge_font_size: int = 9
    badge_pad_x: int = 14
    badge_pad_y: int = 3

    virtual_mode_text: str = 'Virtual Firmware Mode'
    virtual_font_size: int = 9
    virtual_pad_x: tuple[int, int] = (6, 12)

    btn_ping_text: str = 'Ping'
    btn_ping_font_size: int = 8
    btn_ping_pad_x: int = 10
    btn_ping_pad_y: int = 2
