# -*- coding: UTF-8 -*-

'''
Module
    console_panel_style_test.py
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
    Unit tests for ConsolePanelStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.console.console_panel_style import (
    ConsolePanelStyle
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConsolePanelStyle(TestCase):
    '''
        Test cases for ConsolePanelStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default layout and dimension values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default layout and dimension values.'''
        style = ConsolePanelStyle()
        self.assertEqual(style.panel_pad_x, 10)
        self.assertEqual(style.panel_pad_y, 8)
        self.assertEqual(style.title_text, 'SERIAL MONITOR & COMMAND CONSOLE')
        self.assertEqual(style.btn_clear_text, 'Clear')
        self.assertEqual(style.btn_copy_text, 'Copy')
        self.assertEqual(style.btn_select_all_text, 'Select All')
        self.assertEqual(style.prompt_text, 'cmd >')
        self.assertEqual(style.btn_send_text, 'Send')
        self.assertEqual(style.default_log_height, 7)
        self.assertEqual(style.arrow_tx, '-> ')
        self.assertEqual(style.arrow_rx, '<- ')
        self.assertEqual(style.text_wrap_mode, 'none')
        self.assertEqual(style.text_state_disabled, 'disabled')
        self.assertEqual(style.text_state_normal, 'normal')
        self.assertEqual(style.start_index, '1.0')
        self.assertEqual(style.dir_tx, 'TX')
        self.assertEqual(style.key_ctrl_a_lower, '<Control-a>')
        self.assertIn('{timestamp}', style.timestamp_template)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = ConsolePanelStyle()
        with self.assertRaises(FrozenInstanceError):
            style.panel_pad_x = 15  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = ConsolePanelStyle(title_text='CUSTOM CONSOLE', default_log_height=10)
        self.assertEqual(custom_style.title_text, 'CUSTOM CONSOLE')
        self.assertEqual(custom_style.default_log_height, 10)


if __name__ == '__main__':
    main()
