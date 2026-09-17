# -*- coding: UTF-8 -*-

'''
Module
    mecha_editor_tab.py
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
    Dedicated Mecha DSL script editor, linter, and compiler tab container.
'''

from __future__ import annotations

from tkinter import BOTH, BOTTOM, TOP, Widget, X, Frame
from typing import Callable

from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)
from mecharmory.core.service.dsl.mecha_dsl_service import MechaDslService
from mecharmory.infrastructure.gui.theme.theme_manager import ThemeManager
from mecharmory.infrastructure.gui.dsl.mecha_code_editor import MechaCodeEditor
from mecharmory.infrastructure.gui.dsl.mecha_console_view import MechaConsoleView
from mecharmory.infrastructure.gui.dsl.mecha_document_manager import (
    MechaDocumentManager,
)
from mecharmory.infrastructure.gui.dsl.mecha_editor_toolbar import (
    MechaEditorToolbar,
)
from mecharmory.infrastructure.gui.dsl.mecha_example_catalog import (
    MechaExampleCatalog,
)
from mecharmory.infrastructure.gui.dsl.mecha_stream_runner import (
    MechaStreamRunner,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaEditorTab(Frame):
    '''
        Composite tab widget integrating toolbar, code editor, diagnostics, and compiler execution.

        It defines:

            :attributes:
                | _dsl_service - MechaDslService pipeline instance.
                | _doc_manager - MechaDocumentManager file handler.
                | _stream_runner - MechaStreamRunner execution engine.
                | _toolbar - MechaEditorToolbar instance.
                | _editor - MechaCodeEditor instance.
                | _console - MechaConsoleView instance.
                | _on_send_command - Callback dispatching commands to robot.
                | _model - Optional IArmModel for kinematic verification.
            :methods:
                | __init__ - Configures and packs editor tab subcomponents.
                | load_script - Replaces editor text.
                | get_script - Returns active editor buffer content.
                | validate_code - Runs linter and reports to console.
                | compile_code - Translates active code into firmware commands.
                | run_script - Starts streaming execution on background thread.
                | stop_script - Signals streamer to stop.
    '''

    _dsl_service: MechaDslService
    _doc_manager: MechaDocumentManager
    _stream_runner: MechaStreamRunner
    _toolbar: MechaEditorToolbar
    _editor: MechaCodeEditor
    _console: MechaConsoleView
    _on_send_command: Callable[[str], None] | None
    _model: IArmModel | None

    def __init__(
        self,
        parent: Widget,
        dsl_service: MechaDslService | None = None,
        on_send_command: Callable[[str], None] | None = None,
        model: IArmModel | None = None,
        **kwargs: object
    ) -> None:
        '''
            Configures and mounts editor tab subcomponents.

            :param parent: Parent container widget.
            :param dsl_service: Optional MechaDslService instance.
            :param on_send_command: Optional transmission callback.
            :param model: Optional active IArmModel instance.
        '''
        super().__init__(parent, bg=ThemeManager.BG_DARK, **kwargs)
        self._dsl_service = dsl_service or MechaDslService()
        self._doc_manager = MechaDocumentManager()
        self._stream_runner = MechaStreamRunner()
        self._on_send_command = on_send_command
        self._model = model

        self._toolbar = MechaEditorToolbar(
            self,
            on_new=self._on_new,
            on_open=self._on_open,
            on_save=self._on_save,
            on_example_selected=self._on_example_selected,
            on_validate=self.validate_code,
            on_compile=self.compile_code,
            on_run=self.run_script,
            on_stop=self.stop_script
        )
        self._toolbar.pack(fill=X, side=TOP)

        self._console = MechaConsoleView(self, height=5)
        self._console.pack(fill=X, side=BOTTOM, pady=(4, 0))

        self._editor = MechaCodeEditor(self)
        self._editor.pack(fill=BOTH, expand=True, side=TOP)

        # Load default demonstration script
        default_demo = MechaExampleCatalog.get_example('Pick & Place Routine')
        self._editor.set_text(default_demo)

    def load_script(self, text: str) -> None:
        '''Loads given text into editor.'''
        self._editor.set_text(text)

    def get_script(self) -> str:
        '''Returns active editor text.'''
        return self._editor.get_text()

    def validate_code(self) -> bool:
        '''Validates code and displays diagnostics in console.'''
        source = self.get_script()
        diags = self._dsl_service.lint(source=source, model=self._model)
        self._console.show_diagnostics(diags)
        return not any(d.severity == MechaDiagnosticSeverity.ERROR for d in diags)

    def compile_code(self) -> tuple[str, ...]:
        '''Compiles code into firmware commands.'''
        source = self.get_script()
        diags, commands = self._dsl_service.validate_and_compile(
            source=source, model=self._model
        )
        self._console.show_diagnostics(diags)
        if commands:
            self._console.append_message(
                f'🚀 Successfully compiled {len(commands)} firmware instructions.',
                'success'
            )
            for cmd in commands:
                self._console.append_message(f'   > {cmd}', 'info')
        return commands

    def run_script(self) -> None:
        '''Compiles and streams script execution to robot.'''
        commands = self.compile_code()
        if not commands:
            return

        if not self._on_send_command:
            self._console.append_message('⚠️ No active serial connection to dispatch commands.', 'warning')
            return

        self._toolbar.set_running_state(True)
        self._console.append_message('▶️ Streaming script execution to arm...', 'info')
        self._stream_runner.start(
            commands=commands,
            send_fn=self._on_send_command,
            on_finish=lambda: self._toolbar.set_running_state(False)
        )

    def stop_script(self) -> None:
        '''Aborts active stream execution.'''
        self._stream_runner.stop()
        self._toolbar.set_running_state(False)
        if self._on_send_command:
            self._on_send_command('STOP')
        self._console.append_message('⏹️ Script execution stopped by user.', 'warning')

    def _on_new(self) -> None:
        '''Clears editor for a new script.'''
        self._editor.clear()
        self._console.clear()

    def _on_open(self) -> None:
        '''Opens file dialog and loads script.'''
        res = self._doc_manager.open_file()
        if res:
            content, path = res
            self._editor.set_text(content)
            self._console.append_message(f'📂 Loaded {path.name}', 'info')

    def _on_save(self) -> None:
        '''Saves active script.'''
        path = self._doc_manager.save_file(self.get_script())
        if path:
            self._console.append_message(f'💾 Saved {path.name}', 'success')

    def _on_example_selected(self, name: str) -> None:
        '''Loads selected example script from catalog.'''
        script = MechaExampleCatalog.get_example(name)
        if script:
            self._editor.set_text(script)
            self._console.append_message(f'📚 Loaded example: {name}', 'info')
