# -*- coding: UTF-8 -*-

'''
Module
    imecha_dsl_service.py
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
    Defines unified orchestration protocol IMechaDslService for Mecha DSL processing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.dsl.token.mecha_token import MechaToken
from mecharmory.core.model.dsl.ast.imecha_program import IMechaProgram
from mecharmory.core.model.dsl.diagnostic.imecha_diagnostic import IMechaDiagnostic

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMechaDslService(Protocol):
    '''
        High-level orchestration service interface for Mecha DSL.

        It defines:

            :methods:
                | tokenize - Converts source text into lexical tokens.
                | parse - Parses source into AST program hierarchy.
                | lint - Validates syntax, symbols, and kinematic boundaries.
                | compile - Translates valid source text into serial commands.
                | validate_and_compile - Atomically checks and compiles script.
    '''

    def tokenize(self, *, source: str) -> tuple[MechaToken, ...]:
        '''
            Tokenizes source text into a stream of lexical tokens.

            :param source: Raw Mecha DSL script string.
            :return: Tuple of MechaToken items.
        '''

    def parse(self, *, source: str) -> IMechaProgram:
        '''
            Parses raw script text into AST program.

            :param source: Raw Mecha DSL script string.
            :return: IMechaProgram AST root.
        '''

    def lint(
        self,
        *,
        source: str,
        model: IArmModel | None = None
    ) -> tuple[IMechaDiagnostic, ...]:
        '''
            Performs syntax and kinematic validation on source code.

            :param source: Raw Mecha DSL script string.
            :param model: Optional IArmModel instance.
            :return: Tuple of diagnostic feedback items.
        '''

    def compile(self, *, source: str) -> tuple[str, ...]:
        '''
            Compiles source code into executable ASCII serial command lines.

            :param source: Raw Mecha DSL script string.
            :return: Tuple of command strings.
        '''

    def validate_and_compile(
        self,
        *,
        source: str,
        model: IArmModel | None = None
    ) -> tuple[tuple[IMechaDiagnostic, ...], tuple[str, ...]]:
        '''
            Validates and compiles source code in a single atomic pipeline step.

            :param source: Raw Mecha DSL script string.
            :param model: Optional IArmModel instance.
            :return: Tuple of (diagnostics, compiled_commands).
        '''
