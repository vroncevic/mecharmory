# -*- coding: UTF-8 -*-

'''
Module
    mecha_kinematic_bounds_checker.py
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
    Validates joint angles and speeds against hardware calibration limits.
'''

from __future__ import annotations

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.arm.arm_config_defaults import ArmConfigDefaults
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic import MechaDiagnostic
from mecharmory.core.model.dsl.diagnostic.mecha_diagnostic_severity import (
    MechaDiagnosticSeverity,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaKinematicBoundsChecker:
    '''
        Checks physical boundaries, angles, and speeds for 6-DOF manipulator joints.

        It defines:

            :methods:
                | resolve_joint - Maps string joint name or index to JointId.
                | check_angle - Verifies angle falls within joint min_deg and max_deg.
                | check_speed - Verifies speed value is strictly positive.
    '''

    _JOINT_MAP: dict[str, JointId] = {
        '0': JointId.BASE,
        'BASE': JointId.BASE,
        'TRUP': JointId.BASE,
        '1': JointId.LIFT_1,
        'LIFT_1': JointId.LIFT_1,
        'SHOULDER': JointId.LIFT_1,
        'RAME_LEVO': JointId.LIFT_1,
        '2': JointId.LIFT_2,
        'LIFT_2': JointId.LIFT_2,
        'ELBOW': JointId.LIFT_2,
        'RAME_DESNO': JointId.LIFT_2,
        '3': JointId.TUBE_ROLL,
        'TUBE_ROLL': JointId.TUBE_ROLL,
        'ROLL': JointId.TUBE_ROLL,
        'LAKAT': JointId.TUBE_ROLL,
        '4': JointId.END_PITCH,
        'END_PITCH': JointId.END_PITCH,
        'PITCH': JointId.END_PITCH,
        'ZGLOB': JointId.END_PITCH,
        '5': JointId.TOOL_ROLL,
        'TOOL_ROLL': JointId.TOOL_ROLL,
        'TOOL': JointId.TOOL_ROLL,
        'GRIPPER': JointId.TOOL_ROLL
    }

    @classmethod
    def resolve_joint(cls, name_or_idx: str) -> JointId | None:
        '''
            Resolves joint alias string into JointId.

            :param name_or_idx: String identifier or index.
            :return: JointId enum member or None if unknown.
        '''
        return cls._JOINT_MAP.get(str(name_or_idx).upper())

    @classmethod
    def check_angle(
        cls,
        joint_id: JointId,
        angle: float,
        line: int,
        col: int = 1,
        configs: dict[JointId, JointConfig] | None = None
    ) -> MechaDiagnostic | None:
        '''
            Verifies joint angle against min and max calibration boundaries.

            :param joint_id: Target joint ID.
            :param angle: Desired angle in degrees.
            :param line: Source code line index.
            :param col: Source column offset.
            :param configs: Optional custom joint configs mapping.
            :return: MechaDiagnostic if out of bounds, otherwise None.
        '''
        cfg_map = configs if configs is not None else ArmConfigDefaults.get_default_configs()
        cfg = cfg_map.get(joint_id)
        if cfg is None:
            return None

        if angle < cfg.min_deg or angle > cfg.max_deg:
            return MechaDiagnostic(
                line=line,
                column=col,
                message=(
                    f"Joint {joint_id.name} angle {angle:.1f}° is outside safe range "
                    f"[{cfg.min_deg:.1f}°, {cfg.max_deg:.1f}°]"
                ),
                severity=MechaDiagnosticSeverity.ERROR,
                code='KIN001'
            )
        return None

    @classmethod
    def check_speed(cls, speed: float, line: int, col: int = 1) -> MechaDiagnostic | None:
        '''
            Verifies speed parameter value is positive.

            :param speed: Speed in deg/s.
            :param line: Source line number.
            :param col: Source column offset.
            :return: MechaDiagnostic if invalid, otherwise None.
        '''
        if speed <= 0.0:
            return MechaDiagnostic(
                line=line,
                column=col,
                message=f'Speed value must be positive (got {speed})',
                severity=MechaDiagnosticSeverity.ERROR,
                code='KIN002'
            )
        return None
