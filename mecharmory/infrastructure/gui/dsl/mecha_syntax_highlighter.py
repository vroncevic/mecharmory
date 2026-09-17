# -*- coding: UTF-8 -*-

'''
Module
    mecha_syntax_highlighter.py
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
    Syntax highlighter for Mecha DSL applying formatting tags to Tkinter Text widget.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from tkinter import END, Text
from typing import ClassVar

from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaSyntaxHighlighter:
    '''
        Applies syntax color tags to Mecha DSL source code inside a Tkinter Text editor.

        It defines:

            :attributes:
                | _commands - Set of recognized command keywords.
                | _keywords - Set of secondary keywords and joint names.
                | _re_comment - Regex pattern for line comments.
                | _re_number - Regex pattern for numeric literals.
                | _re_word - Regex pattern for identifiers.
            :methods:
                | __init__ - Configures style tags on the target text widget.
                | highlight - Scans and colors text widget content.
    '''

    _commands: ClassVar[frozenset[str]] = frozenset(
        cmd.value for cmd in MechaCommandType
    )

    _keywords: ClassVar[frozenset[str]] = frozenset({
        'OPEN', 'CLOSE', 'BASE', 'LIFT_1', 'LIFT_2', 'TUBE_ROLL', 'END_PITCH',
        'TOOL_ROLL', 'SHOULDER', 'ELBOW', 'ROLL', 'PITCH', 'TOOL', 'GRIPPER',
        'HOME', 'PARKED', 'PARK', 'FORWARD_REACH', 'REACH', 'HIGH_REACH'
    })

    _re_comment: ClassVar[Pattern[str]] = re_compile(r'[#;].*$')
    _re_number: ClassVar[Pattern[str]] = re_compile(r'\b[-+]?[0-9]*\.?[0-9]+\b')
    _re_word: ClassVar[Pattern[str]] = re_compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')

    def __init__(self, text_widget: Text) -> None:
        '''
            Configures style tags on the target Text widget.

            :param text_widget: Tkinter Text widget to format.
        '''
        text_widget.tag_configure(
            'dsl_comment',
            foreground=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 10, 'italic')
        )
        text_widget.tag_configure(
            'dsl_command',
            foreground=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 10, 'bold')
        )
        text_widget.tag_configure(
            'dsl_keyword',
            foreground=ThemeManager.ACCENT_BLUE,
            font=(ThemeManager.FONT_MONO, 10, 'bold')
        )
        text_widget.tag_configure(
            'dsl_number',
            foreground=ThemeManager.ACCENT_GREEN,
            font=(ThemeManager.FONT_MONO, 10)
        )
        text_widget.tag_configure(
            'dsl_identifier',
            foreground=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_MONO, 10)
        )

    def highlight(self, text_widget: Text) -> None:
        '''
            Performs complete syntax color update on text widget contents.

            :param text_widget: Target text widget.
        '''
        content = text_widget.get('1.0', END)
        for tag in ('dsl_comment', 'dsl_command', 'dsl_keyword', 'dsl_number', 'dsl_identifier'):
            text_widget.tag_remove(tag, '1.0', END)

        lines = content.split('\n')
        for line_idx, line in enumerate(lines, start=1):
            if not line:
                continue

            comment_match = self._re_comment.search(line)
            end_col = comment_match.start() if comment_match else len(line)

            for match in self._re_word.finditer(line[:end_col]):
                word = match.group()
                word_upper = word.upper()
                start_pos = f'{line_idx}.{match.start()}'
                end_pos = f'{line_idx}.{match.end()}'

                if word_upper in self._commands:
                    text_widget.tag_add('dsl_command', start_pos, end_pos)
                elif word_upper in self._keywords:
                    text_widget.tag_add('dsl_keyword', start_pos, end_pos)
                else:
                    text_widget.tag_add('dsl_identifier', start_pos, end_pos)

            for match in self._re_number.finditer(line[:end_col]):
                start_pos = f'{line_idx}.{match.start()}'
                end_pos = f'{line_idx}.{match.end()}'
                text_widget.tag_add('dsl_number', start_pos, end_pos)

            if comment_match:
                start_pos = f'{line_idx}.{comment_match.start()}'
                end_pos = f'{line_idx}.{len(line)}'
                text_widget.tag_add('dsl_comment', start_pos, end_pos)
