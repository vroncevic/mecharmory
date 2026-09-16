# -*- coding: UTF-8 -*-

'''
Module
    serial_panel_style_test.py
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
    Unit tests for SerialPanelStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.serial.serial_panel_style import (
    SerialPanelStyle
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialPanelStyle(TestCase):
    '''
        Test cases for SerialPanelStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default layout and dimension values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default layout and dimension values.'''
        style = SerialPanelStyle()
        self.assertEqual(style.bar_height, 44)
        self.assertEqual(style.bar_pad_x, 12)
        self.assertEqual(style.bar_pad_y, 6)
        self.assertEqual(style.title_text, 'Mecharmo 6-DOF')
        self.assertEqual(style.port_combo_width, 15)
        self.assertEqual(style.btn_scan_text, 'Scan')
        self.assertEqual(style.default_baud, 115200)
        self.assertEqual(style.btn_connect_text, 'Connect')
        self.assertEqual(style.btn_disconnect_text, 'Disconnect')
        self.assertEqual(style.btn_disconnect_fg, '#ffffff')
        self.assertEqual(style.connect_btn_spacing_x, (0, 12))
        self.assertEqual(style.status_disconnected_text, 'Disconnected')
        self.assertEqual(style.label_font_size, 9)
        self.assertEqual(style.combo_state, 'readonly')
        self.assertEqual(style.btn_scan_font_size, 8)
        self.assertEqual(style.btn_scan_pad_y, 2)
        self.assertEqual(style.btn_ping_text, 'Ping')
        self.assertIn('/dev/ttyACM0', style.fallback_ports)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = SerialPanelStyle()
        with self.assertRaises(FrozenInstanceError):
            style.bar_height = 50  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = SerialPanelStyle(title_text='CUSTOM SERIAL', default_baud=9600)
        self.assertEqual(custom_style.title_text, 'CUSTOM SERIAL')
        self.assertEqual(custom_style.default_baud, 9600)


if __name__ == '__main__':
    main()
