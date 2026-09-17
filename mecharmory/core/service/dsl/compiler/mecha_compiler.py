# -*- coding: UTF-8 -*-

'''
Module
    mecha_compiler.py
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
    Concrete compiler translating Mecha DSL program AST into firmware ASCII command lines.
'''

from __future__ import annotations

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.arm_preset_defaults import ArmPresetDefaults
from mecharmory.core.model.dsl.ast.mecha_command_type import MechaCommandType
from mecharmory.core.model.dsl.ast.mecha_instruction import MechaInstruction
from mecharmory.core.model.dsl.ast.mecha_program import MechaProgram
from mecharmory.core.service.arm.arm_command_formatter import ArmCommandFormatter
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


class MechaCompiler:
    '''
        Translates MechaProgram AST instructions into ASCII serial command sequences.

        It defines:

            :methods:
                | compile - Converts program AST into sequence of firmware commands.
                | _compile_move_p - Translates multi-axis move into SETP.
                | _compile_move_j - Translates single-axis move into SET.
                | _compile_preset - Translates posture preset into SETP.
                | _compile_gripper - Translates gripper action into SET on Joint 5.
    '''

    def compile(self, *, program: MechaProgram) -> tuple[str, ...]:
        '''
            Compiles MechaProgram into sequence of firmware command strings.

            :param program: Parsed MechaProgram AST.
            :return: Tuple of executable ASCII command lines.
        '''
        lines: list[str] = []

        for instr in program.instructions:
            match instr.command_type:
                case MechaCommandType.MOVE_P:
                    cmd = self._compile_move_p(instr, program)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.MOVE_J:
                    cmd = self._compile_move_j(instr, program)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.PRESET:
                    cmd = self._compile_preset(instr)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.SPEED:
                    lines.extend(self._compile_speed(instr, program))
                case MechaCommandType.SPEED_JOINT:
                    cmd = self._compile_speed_joint(instr, program)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.GRIPPER:
                    cmd = self._compile_gripper(instr, program)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.TOOL_ROLL:
                    cmd = self._compile_tool_roll(instr, program)
                    if cmd:
                        lines.append(cmd)
                case MechaCommandType.WAIT_MS:
                    ms = self._resolve_num(instr.parameters.get('args', [0]), program)
                    lines.append(f'WAIT {int(ms)}')
                case MechaCommandType.HOME:
                    lines.append(ArmCommandFormatter.format_home())
                case MechaCommandType.STOP:
                    lines.append(ArmCommandFormatter.format_stop())
                case MechaCommandType.STATUS:
                    lines.append(ArmCommandFormatter.format_status())
                case MechaCommandType.PING:
                    lines.append('PING')
                case _:
                    pass

        return tuple(lines)

    def _compile_move_p(self, instr: MechaInstruction, program: MechaProgram) -> str | None:
        '''Translates MOVE_P into SETP command.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            return None

        first = str(args[0]).upper()
        if first in program.points:
            coords = list(program.points[first])
            return ArmCommandFormatter.format_setp(coords)

        if len(args) >= 6:
            coords = [float(self._resolve_num([args[i]], program)) for i in range(6)]
            return ArmCommandFormatter.format_setp(coords)
        return None

    def _compile_move_j(self, instr: MechaInstruction, program: MechaProgram) -> str | None:
        '''Translates MOVE_J into SET command.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or len(args) < 2:
            return None

        jid = MechaKinematicBoundsChecker.resolve_joint(args[0])
        if jid is None:
            return None

        angle = float(self._resolve_num([args[1]], program))
        return ArmCommandFormatter.format_set(jid, angle)

    def _compile_preset(self, instr: MechaInstruction) -> str | None:
        '''Translates PRESET into SETP command.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            return None

        name = str(args[0]).upper()
        match name:
            case 'HOME':
                preset = ArmPresetDefaults.get_home_preset()
            case 'PARKED' | 'PARK':
                preset = ArmPresetDefaults.get_parked_preset()
            case 'FORWARD_REACH' | 'REACH':
                preset = ArmPresetDefaults.get_forward_reach_preset()
            case 'HIGH_REACH':
                preset = ArmPresetDefaults.get_high_reach_preset()
            case _:
                return None

        return ArmCommandFormatter.format_setp(list(preset.angles))

    def _compile_speed(self, instr: MechaInstruction, program: MechaProgram) -> list[str]:
        '''Translates SPEED into SPEED commands for all 6 axes.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or not args:
            return []
        val = float(self._resolve_num([args[0]], program))
        return [ArmCommandFormatter.format_speed(jid, val) for jid in JointId]

    def _compile_speed_joint(self, instr: MechaInstruction, program: MechaProgram) -> str | None:
        '''Translates SPEED_JOINT into single-axis SPEED command.'''
        args = instr.parameters.get('args', [])
        if not isinstance(args, list) or len(args) < 2:
            return None
        jid = MechaKinematicBoundsChecker.resolve_joint(args[0])
        if jid is None:
            return None
        val = float(self._resolve_num([args[1]], program))
        return ArmCommandFormatter.format_speed(jid, val)

    def _compile_gripper(self, instr: MechaInstruction, program: MechaProgram) -> str | None:
        '''Translates GRIPPER into SET command on Joint 5.'''
        args = instr.parameters.get('args', [])
        sub = str(args[0]).upper() if args else 'CLOSE'
        if sub == 'OPEN':
            return ArmCommandFormatter.format_set(JointId.TOOL_ROLL, 180.0)
        if sub == 'CLOSE':
            return ArmCommandFormatter.format_set(JointId.TOOL_ROLL, 0.0)
        angle = float(self._resolve_num(args, program))
        return ArmCommandFormatter.format_set(JointId.TOOL_ROLL, angle)

    def _compile_tool_roll(self, instr: MechaInstruction, program: MechaProgram) -> str | None:
        '''Translates TOOL_ROLL into SET command on Joint 5.'''
        args = instr.parameters.get('args', [])
        if not args:
            return None
        angle = float(self._resolve_num(args, program))
        return ArmCommandFormatter.format_set(JointId.TOOL_ROLL, angle)

    def _resolve_num(self, args: list[object], program: MechaProgram) -> float:
        '''Resolves numeric value from argument token or variable symbol table.'''
        if not args:
            return 0.0
        val_str = str(args[0]).upper()
        if val_str in program.variables:
            return program.variables[val_str]
        try:
            return float(val_str)
        except ValueError:
            return 0.0
