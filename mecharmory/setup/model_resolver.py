# -*- coding: UTF-8 -*-

'''
Module
    model_resolver.py
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
    Model resolver for constructing ArmModel domain instance from configuration data.
'''

from __future__ import annotations

from typing import Any
from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.model.arm.arm_model import ArmModel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryModelResolver:
    '''
        Resolver building domain ArmModel with kinematics configs and presets from raw data.

        It defines:

            :methods:
                | resolve_model - Resolves ArmModel from loaded configuration dictionary.
    '''

    _JOINT_NAMES: dict[JointId, str] = {
        JointId.BASE: 'J0: Base (Yaw)',
        JointId.LIFT_1: 'J1: Shoulder Left (Pitch)',
        JointId.LIFT_2: 'J2: Shoulder Right (Pitch)',
        JointId.TUBE_ROLL: 'J3: Elbow (Roll)',
        JointId.END_PITCH: 'J4: Wrist (Pitch)',
        JointId.TOOL_ROLL: 'J5: Tool (Roll)',
    }

    @classmethod
    def resolve_model(cls, config_data: dict[str, Any]) -> ArmModel:
        '''
            Resolves ArmModel from loaded configuration dictionary.

            :param config_data: Loaded configuration dictionary.
            :return: Configured ArmModel instance.
            :exceptions: None.
        '''
        if not config_data:
            return ArmModel()

        configs: dict[JointId, JointConfig] = {}
        for jid in JointId:
            prefix: str = f'j{int(jid)}_'
            configs[jid] = JointConfig(
                joint_id=jid,
                name=cls._JOINT_NAMES[jid],
                channel=int(config_data.get(f'{prefix}channel', int(jid))),
                min_deg=float(
                    config_data.get(f'{prefix}min_deg', 0.0 if int(jid) in (0, 3, 5) else 15.0)
                ),
                max_deg=float(
                    config_data.get(f'{prefix}max_deg', 180.0 if int(jid) in (0, 3, 5) else 165.0)
                ),
                home_deg=float(config_data.get(f'{prefix}home_deg', 90.0)),
                default_speed_deg_s=float(config_data.get(f'{prefix}speed_deg_s', 60.0)),
                min_pulse_us=int(config_data.get(f'{prefix}min_pulse_us', 500)),
                max_pulse_us=int(config_data.get(f'{prefix}max_pulse_us', 2500))
            )

        presets_raw: list[dict[str, Any]] = config_data.get('presets', [])
        presets: list[MotionPreset] = []
        for p in presets_raw:
            presets.append(
                MotionPreset(
                    name=str(p.get('name', 'Preset')),
                    description=str(p.get('description', '')),
                    angles=tuple(float(a) for a in p.get('angles', [90.0] * 6))
                )
            )

        return ArmModel(
            configs=configs if configs else None,
            presets=tuple(presets) if presets else None
        )
