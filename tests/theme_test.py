# -*- coding: UTF-8 -*-

'''
Module
    theme_test.py
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
    Unit tests for ThemeManager constants.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestThemeManager(TestCase):
    '''
        Test cases for ThemeManager styling constants.

        It defines:

            :methods:
                | test_color_definitions - Tests presence and hex format of theme color tokens.
                | test_font_definitions - Tests typography font family definitions.
    '''

    def test_color_definitions(self) -> None:
        '''Tests presence and hex format of theme color tokens.'''
        self.assertTrue(ThemeManager.BG_DARK.startswith('#'))
        self.assertTrue(ThemeManager.BG_PANEL.startswith('#'))
        self.assertTrue(ThemeManager.BG_CANVAS.startswith('#'))
        self.assertTrue(ThemeManager.ACCENT_CYAN.startswith('#'))
        self.assertTrue(ThemeManager.ACCENT_RED.startswith('#'))

    def test_font_definitions(self) -> None:
        '''Tests typography font family definitions.'''
        self.assertEqual(ThemeManager.FONT_FAMILY, 'Segoe UI')
        self.assertEqual(ThemeManager.FONT_MONO, 'Consolas')


if __name__ == '__main__':
    main()
