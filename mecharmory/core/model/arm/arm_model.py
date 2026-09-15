# -*- coding: UTF-8 -*-

'''
Module
    arm_model.py
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
    Aggregate root holding configurations, runtime states, and presets for Mecharmo.
'''

from __future__ import annotations

from typing import Iterable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.kinematics.joint_state import JointState
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.model.arm.arm_config_defaults import ArmConfigDefaults
from mecharmory.core.model.arm.arm_preset_defaults import ArmPresetDefaults

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmModel:
    '''
        Domain aggregate root for the 6-DOF robotic manipulator.

        It defines:

            :attributes:
                | _configs - Mapping of JointId to static calibration JointConfig.
                | _states - Mapping of JointId to dynamic runtime JointState.
                | _presets - Tuple of predefined postures.
            :methods:
                | __init__ - Configures joint calibration and initial postures.
                | get_config - Retrieves configuration for a joint.
                | get_state - Retrieves current state for a joint.
                | get_all_states - Returns an iterable of all active joint states.
                | get_presets - Returns available postures.
                | clamp_angle - Constrains angle value within joint boundaries.
                | update_target - Sets desired angle for a joint after validation.
                | update_current - Updates actual reported angle.
    '''

    _configs: dict[JointId, JointConfig]
    _states: dict[JointId, JointState]
    _presets: tuple[MotionPreset, ...]

    def __init__(
        self,
        configs: dict[JointId, JointConfig] | None = None,
        presets: tuple[MotionPreset, ...] | None = None
    ) -> None:
        '''
            Initializes joint models matching physical hardware assembly.

            :param configs: Optional custom joint configurations.
            :param presets: Optional custom motion presets.
            :exceptions: None.
        '''
        self._configs = configs if configs is not None else ArmConfigDefaults.get_default_configs()
        self._presets = presets if presets is not None else ArmPresetDefaults.get_default_presets()

        self._states = {
            jid: JointState(
                joint_id=jid,
                current_angle=cfg.home_deg,
                target_angle=cfg.home_deg,
                speed_deg_s=cfg.default_speed_deg_s,
                is_moving=False
            )
            for jid, cfg in self._configs.items()
        }

    def get_config(self, joint_id: JointId) -> JointConfig:
        '''
            Fetches configuration metadata for given joint.

            :param joint_id: Target joint ID.
            :return: JointConfig object.
            :exceptions: None.
        '''
        return self._configs[joint_id]

    def get_state(self, joint_id: JointId) -> JointState:
        '''
            Fetches dynamic state for given joint.

            :param joint_id: Target joint ID.
            :return: JointState object.
            :exceptions: None.
        '''
        return self._states[joint_id]

    def get_all_states(self) -> Iterable[JointState]:
        '''
            Returns list of all joint states ordered by JointId.

            :return: Iterable of JointState.
            :exceptions: None.
        '''
        return self._states.values()

    def get_presets(self) -> tuple[MotionPreset, ...]:
        '''
            Returns available motion presets.

            :return: Tuple of MotionPreset.
            :exceptions: None.
        '''
        return self._presets

    def clamp_angle(self, joint_id: JointId, angle: float) -> float:
        '''
            Clamps angle to safe configured physical range.

            :param joint_id: Target joint ID.
            :param angle: Commanded angle value.
            :return: Clamped angle value in degrees.
            :exceptions: None.
        '''
        cfg: JointConfig = self._configs[joint_id]
        if angle < cfg.min_deg:
            return cfg.min_deg
        if angle > cfg.max_deg:
            return cfg.max_deg
        return angle

    def update_target(self, joint_id: JointId, angle: float) -> float:
        '''
            Updates target angle for joint with limit clamping.

            :param joint_id: Target joint ID.
            :param angle: Desired angle.
            :return: Clamped angle applied to target.
            :exceptions: None.
        '''
        clamped: float = self.clamp_angle(joint_id, angle)
        self._states[joint_id].target_angle = clamped
        return clamped

    def update_current(self, joint_id: JointId, angle: float) -> None:
        '''
            Updates current reported angle.

            :param joint_id: Target joint ID.
            :param angle: Reported angle.
            :exceptions: None.
        '''
        self._states[joint_id].current_angle = self.clamp_angle(joint_id, angle)
