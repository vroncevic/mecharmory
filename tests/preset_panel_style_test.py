# -*- coding: UTF-8 -*-

'''
Module
    preset_panel_style_test.py
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
    Unit tests for PresetPanelStyle configuration model.
'''

from __future__ import annotations

from unittest import TestCase, main
from dataclasses import FrozenInstanceError

from mecharmory.infrastructure.gui.preset.preset_panel_style import (
    PresetPanelStyle
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPresetPanelStyle(TestCase):
    '''
        Test cases for PresetPanelStyle dataclass.

        It defines:

            :methods:
                | test_default_values - Verifies default layout and dimension values.
                | test_frozen_immutability - Verifies immutability of frozen dataclass.
                | test_custom_values - Verifies custom values initialization.
    '''

    def test_default_values(self) -> None:
        '''Verifies default layout and dimension values.'''
        style = PresetPanelStyle()
        self.assertEqual(style.panel_pad_x, 12)
        self.assertEqual(style.panel_pad_y, 6)
        self.assertEqual(style.title_text, 'POSTURE PRESETS:')
        self.assertEqual(style.title_font_size, 8)
        self.assertEqual(style.title_font_weight, 'bold')
        self.assertEqual(style.btn_pad_x, 10)
        self.assertEqual(style.btn_pad_y, 3)

    def test_frozen_immutability(self) -> None:
        '''Verifies immutability of frozen dataclass.'''
        style = PresetPanelStyle()
        with self.assertRaises(FrozenInstanceError):
            style.panel_pad_x = 20  # type: ignore

    def test_custom_values(self) -> None:
        '''Verifies custom values initialization.'''
        custom_style = PresetPanelStyle(title_text='CUSTOM PRESETS:', panel_pad_x=16)
        self.assertEqual(custom_style.title_text, 'CUSTOM PRESETS:')
        self.assertEqual(custom_style.panel_pad_x, 16)


if __name__ == '__main__':
    main()
