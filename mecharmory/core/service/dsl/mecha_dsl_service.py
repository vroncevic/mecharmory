# -*- coding: UTF-8 -*-

'''
Module
    mecha_dsl_service.py
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
    Concrete orchestration service coordinating Mecha DSL processing pipeline.
'''

from __future__ import annotations

from typing import Any

from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.dsl.token.mecha_token import MechaToken
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic import MechaDiagnostic
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)
from mecharmory.core.service.dsl.lexer.mecha_lexer import MechaLexer
from mecharmory.core.service.dsl.parser.mecha_parser import MechaParser
from mecharmory.core.service.dsl.linter.mecha_linter import MechaLinter
from mecharmory.core.service.dsl.compiler.mecha_compiler import MechaCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaDslService:
    '''
        Composite service coordinating lexer, parser, linter, and compiler for Mecha DSL.

        It defines:

            :attributes:
                | _lexer - MechaLexer instance.
                | _parser - MechaParser instance.
                | _linter - MechaLinter instance.
                | _compiler - MechaCompiler instance.
            :methods:
                | __init__ - Initializes the processing pipeline collaborators.
                | tokenize - Tokenizes source text.
                | parse - Parses source into program AST.
                | lint - Validates program AST and collects diagnostics.
                | compile - Compiles program AST into firmware commands.
                | validate_and_compile - Atomically performs validation and compilation.
    '''

    _lexer: MechaLexer
    _parser: MechaParser
    _linter: MechaLinter
    _compiler: MechaCompiler

    def __init__(
        self,
        lexer: MechaLexer | None = None,
        parser: MechaParser | None = None,
        linter: MechaLinter | None = None,
        compiler: MechaCompiler | None = None
    ) -> None:
        '''
            Initializes pipeline collaborators with optional dependency injection.

            :param lexer: Optional custom MechaLexer instance.
            :param parser: Optional custom MechaParser instance.
            :param linter: Optional custom MechaLinter instance.
            :param compiler: Optional custom MechaCompiler instance.
        '''
        self._lexer = lexer or MechaLexer()
        self._parser = parser or MechaParser()
        self._linter = linter or MechaLinter()
        self._compiler = compiler or MechaCompiler()

    def tokenize(self, *, source: str) -> tuple[MechaToken, ...]:
        '''
            Tokenizes source text into a stream of lexical tokens.

            :param source: Raw script text.
            :return: Tuple of MechaToken items.
        '''
        return self._lexer.tokenize(source=source)

    def parse(self, *, source: str) -> Any:
        '''
            Parses raw script text into AST program.

            :param source: Raw script text.
            :return: MechaProgram instance.
        '''
        tokens = self.tokenize(source=source)
        return self._parser.parse(tokens=tokens)

    def lint(
        self,
        *,
        source: str,
        model: IArmModel | None = None
    ) -> tuple[Any, ...]:
        '''
            Performs syntax and kinematic validation on source code.

            :param source: Raw script text.
            :param model: Optional IArmModel instance.
            :return: Tuple of diagnostic feedback items.
        '''
        try:
            program = self.parse(source=source)
            return self._linter.lint(program=program, model=model)
        except ValueError as exc:
            return (
                MechaDiagnostic(
                    line=1,
                    column=1,
                    message=str(exc),
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='LEX001'
                ),
            )

    def compile(self, *, source: str) -> tuple[str, ...]:
        '''
            Compiles source code into ASCII serial command lines.

            :param source: Raw script text.
            :return: Tuple of command strings.
        '''
        program = self.parse(source=source)
        return self._compiler.compile(program=program)

    def validate_and_compile(
        self,
        *,
        source: str,
        model: IArmModel | None = None
    ) -> tuple[tuple[Any, ...], tuple[str, ...]]:
        '''
            Validates and compiles source code in a single atomic pipeline step.

            :param source: Raw script text.
            :param model: Optional IArmModel instance.
            :return: Tuple of (diagnostics, compiled_commands).
        '''
        diags = self.lint(source=source, model=model)
        has_errors = any(
            d.severity == MechaDiagnosticSeverity.ERROR for d in diags
        )
        if has_errors:
            return (diags, ())

        commands = self.compile(source=source)
        return (diags, commands)
