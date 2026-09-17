# -*- coding: UTF-8 -*-

'''
Module
    mecha_linter.py
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
    Concrete implementation of static semantic and kinematic linter for Mecha DSL.
'''

from __future__ import annotations

from typing import Any

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.arm_preset_defaults import ArmPresetDefaults
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType
from mecharmory.core.model.dsl.ast.mecha_instruction import MechaInstruction
from mecharmory.core.model.dsl.ast.mecha_program import MechaProgram
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic import MechaDiagnostic
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)
from mecharmory.core.service.dsl.linter.mecha_kinematic_bounds_checker import (
    MechaKinematicBoundsChecker,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaLinter:
    '''
        Semantic and kinematic static analyzer for Mecha DSL programs.

        It defines:

            :methods:
                | lint - Validates program AST and produces diagnostic feedback.
                | _lint_move_p - Validates multi-axis move instruction.
                | _lint_move_j - Validates single joint move instruction.
                | _lint_preset - Validates preset name.
    '''

    def lint(
        self,
        *,
        program: MechaProgram,
        model: IArmModel | None = None
    ) -> tuple[Any, ...]:
        '''
            Performs static semantic and kinematic boundary validation.

            :param program: Parsed MechaProgram AST.
            :param model: Optional active IArmModel instance.
            :return: Tuple of MechaDiagnostic instances.
        '''
        diagnostics: list[MechaDiagnostic] = []

        for instr in program.instructions:
            match instr.command_type:
                case MechaCommandType.MOVE_P:
                    self._lint_move_p(instr, program, diagnostics)
                case MechaCommandType.MOVE_J:
                    self._lint_move_j(instr, program, diagnostics)
                case MechaCommandType.PRESET:
                    self._lint_preset(instr, diagnostics)
                case MechaCommandType.SPEED:
                    self._lint_speed(instr, program, diagnostics)
                case MechaCommandType.WAIT_MS:
                    self._lint_wait(instr, program, diagnostics)
                case _:
                    pass

        return tuple(diagnostics)

    def _lint_move_p(
        self,
        instr: MechaInstruction,
        program: MechaProgram,
        diags: list[MechaDiagnostic]
    ) -> None:
        '''Validates MOVE_P arguments or referenced point posture.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message='MOVE_P requires a POINT identifier or 6 joint angles',
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM001'
                )
            )
            return

        first_arg = str(args[0]).upper()
        if first_arg in program.points:
            coords = program.points[first_arg]
            for jid in JointId:
                diag = MechaKinematicBoundsChecker.check_angle(
                    jid, coords[int(jid)], instr.line_number
                )
                if diag:
                    diags.append(diag)
        elif len(args) >= 6:
            for idx in range(6):
                val_str = str(args[idx]).upper()
                angle = program.variables.get(val_str)
                if angle is None:
                    try:
                        angle = float(val_str)
                    except ValueError:
                        diags.append(
                            MechaDiagnostic(
                                line=instr.line_number,
                                column=1,
                                message=f"Invalid angle or undeclared variable '{val_str}'",
                                severity=MechaDiagnosticSeverity.ERROR,
                                code='SEM002'
                            )
                        )
                        continue
                jid = JointId(idx)
                diag = MechaKinematicBoundsChecker.check_angle(jid, angle, instr.line_number)
                if diag:
                    diags.append(diag)
        else:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message=f"Undefined point or incomplete coordinates '{first_arg}'",
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM003'
                )
            )

    def _lint_move_j(
        self,
        instr: MechaInstruction,
        program: MechaProgram,
        diags: list[MechaDiagnostic]
    ) -> None:
        '''Validates single-axis joint move parameters.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or len(args) < 2:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message='MOVE_J requires joint identifier and target angle',
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM004'
                )
            )
            return

        jid = MechaKinematicBoundsChecker.resolve_joint(args[0])
        if jid is None:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message=f"Unknown joint identifier '{args[0]}'",
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM005'
                )
            )
            return

        val_str = str(args[1]).upper()
        angle = program.variables.get(val_str)
        if angle is None:
            try:
                angle = float(val_str)
            except ValueError:
                diags.append(
                    MechaDiagnostic(
                        line=instr.line_number,
                        column=1,
                        message=f"Invalid angle or undeclared variable '{val_str}'",
                        severity=MechaDiagnosticSeverity.ERROR,
                        code='SEM006'
                    )
                )
                return

        diag = MechaKinematicBoundsChecker.check_angle(jid, angle, instr.line_number)
        if diag:
            diags.append(diag)

    def _lint_preset(self, instr: MechaInstruction, diags: list[MechaDiagnostic]) -> None:
        '''Validates motion preset name existence.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message='PRESET requires preset name (e.g. HOME, PARKED, FORWARD_REACH, HIGH_REACH)',
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM007'
                )
            )
            return

        name = str(args[0]).upper()
        valid_presets = {'HOME', 'PARKED', 'PARK', 'FORWARD_REACH', 'REACH', 'HIGH_REACH'}
        if name not in valid_presets:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message=f"Unknown preset name '{name}'. Available: {sorted(valid_presets)}",
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM008'
                )
            )

    def _lint_speed(
        self,
        instr: MechaInstruction,
        program: MechaProgram,
        diags: list[MechaDiagnostic]
    ) -> None:
        '''Validates SPEED command parameter.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            return
        val_str = str(args[0]).upper()
        spd = program.variables.get(val_str)
        if spd is None:
            try:
                spd = float(val_str)
            except ValueError:
                return
        diag = MechaKinematicBoundsChecker.check_speed(spd, instr.line_number)
        if diag:
            diags.append(diag)

    def _lint_wait(
        self,
        instr: MechaInstruction,
        program: MechaProgram,
        diags: list[MechaDiagnostic]
    ) -> None:
        '''Validates WAIT_MS delay parameter.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            return
        val_str = str(args[0]).upper()
        ms = program.variables.get(val_str)
        if ms is None:
            try:
                ms = float(val_str)
            except ValueError:
                return
        if ms < 0:
            diags.append(
                MechaDiagnostic(
                    line=instr.line_number,
                    column=1,
                    message=f'WAIT_MS delay must be non-negative (got {ms})',
                    severity=MechaDiagnosticSeverity.ERROR,
                    code='SEM009'
                )
            )
