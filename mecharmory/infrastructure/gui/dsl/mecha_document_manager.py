# -*- coding: UTF-8 -*-

'''
Module
    mecha_document_manager.py
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
    Document file manager coordinating open, save, and persistence for Mecha DSL scripts.
'''

from __future__ import annotations

from pathlib import Path
from tkinter.filedialog import askopenfilename, asksaveasfilename

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaDocumentManager:
    '''
        Handles file persistence and dialogs for .mecha script files.

        It defines:

            :attributes:
                | _current_path - Active script file path or None if unsaved.
            :methods:
                | open_file - Prompts user to choose a .mecha file and loads its content.
                | save_file - Saves content to active path or prompts if untitled.
                | save_file_as - Always prompts for destination path and saves content.
                | get_current_path - Returns active Path or None.
    '''

    _current_path: Path | None

    def __init__(self) -> None:
        '''Initializes document manager with no active file.'''
        self._current_path = None

    def open_file(self) -> tuple[str, Path] | None:
        '''
            Prompts user to select a .mecha file and reads its contents.

            :return: Tuple of (file_content, file_path) or None if cancelled.
        '''
        file_path_str = askopenfilename(
            title='Open Mecha Script',
            filetypes=[('Mecha Scripts', '*.mecha'), ('All Files', '*.*')]
        )
        if not file_path_str:
            return None

        path = Path(file_path_str)
        try:
            content = path.read_text(encoding='utf-8')
            self._current_path = path
            return (content, path)
        except OSError:
            return None

    def save_file(self, content: str) -> Path | None:
        '''
            Saves content to current file or prompts if untitled.

            :param content: Script text to write.
            :return: Path where saved or None if cancelled/failed.
        '''
        if self._current_path is not None:
            try:
                self._current_path.write_text(content, encoding='utf-8')
                return self._current_path
            except OSError:
                return None
        return self.save_file_as(content)

    def save_file_as(self, content: str) -> Path | None:
        '''
            Prompts user for destination and saves script content.

            :param content: Script text to write.
            :return: Path where saved or None if cancelled/failed.
        '''
        file_path_str = asksaveasfilename(
            title='Save Mecha Script As',
            defaultextension='.mecha',
            filetypes=[('Mecha Scripts', '*.mecha'), ('All Files', '*.*')]
        )
        if not file_path_str:
            return None

        path = Path(file_path_str)
        try:
            path.write_text(content, encoding='utf-8')
            self._current_path = path
            return path
        except OSError:
            return None

    def get_current_path(self) -> Path | None:
        '''
            Retrieves current active script path.

            :return: Path or None.
        '''
        return self._current_path
