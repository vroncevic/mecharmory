# -*- coding: UTF-8 -*-

'''
Module
    arm_model_test.py
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
    Unit tests for ArmModel domain aggregate.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.arm_model import ArmModel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmModel(TestCase):
    '''
        Test cases for ArmModel domain aggregate.

        It defines:

            :methods:
                | test_arm_model_initialization - Tests default configuration and joint states.
                | test_clamp_angle - Tests boundary clamping for joints.
                | test_update_target - Tests setting target angle with safety limits.
                | test_update_current - Tests setting reported angle with safety limits.
                | test_presets_availability - Tests access to motion presets.
    '''

    def test_arm_model_initialization(self) -> None:
        '''Tests default configuration and joint states.'''
        model = ArmModel()
        for jid in JointId:
            cfg = model.get_config(jid)
            st = model.get_state(jid)
            self.assertEqual(cfg.joint_id, jid)
            self.assertEqual(st.joint_id, jid)
            self.assertEqual(st.current_angle, cfg.home_deg)
            self.assertEqual(st.target_angle, cfg.home_deg)
        all_states = list(model.get_all_states())
        self.assertEqual(len(all_states), 6)

    def test_clamp_angle(self) -> None:
        '''Tests boundary clamping for joints.'''
        model = ArmModel()
        # BASE limits: [0.0, 180.0]
        self.assertEqual(model.clamp_angle(JointId.BASE, -10.0), 0.0)
        self.assertEqual(model.clamp_angle(JointId.BASE, 200.0), 180.0)
        self.assertEqual(model.clamp_angle(JointId.BASE, 90.0), 90.0)
        # LIFT_1 limits: [15.0, 165.0]
        self.assertEqual(model.clamp_angle(JointId.LIFT_1, 5.0), 15.0)
        self.assertEqual(model.clamp_angle(JointId.LIFT_1, 175.0), 165.0)

    def test_update_target(self) -> None:
        '''Tests setting target angle with safety limits.'''
        model = ArmModel()
        clamped = model.update_target(JointId.BASE, 45.0)
        self.assertEqual(clamped, 45.0)
        self.assertEqual(model.get_state(JointId.BASE).target_angle, 45.0)
        clamped_out = model.update_target(JointId.BASE, 250.0)
        self.assertEqual(clamped_out, 180.0)
        self.assertEqual(model.get_state(JointId.BASE).target_angle, 180.0)

    def test_update_current(self) -> None:
        '''Tests setting reported angle with safety limits.'''
        model = ArmModel()
        model.update_current(JointId.LIFT_2, 80.0)
        self.assertEqual(model.get_state(JointId.LIFT_2).current_angle, 80.0)
        model.update_current(JointId.LIFT_2, 0.0)
        self.assertEqual(model.get_state(JointId.LIFT_2).current_angle, 15.0)

    def test_presets_availability(self) -> None:
        '''Tests access to motion presets.'''
        model = ArmModel()
        presets = model.get_presets()
        self.assertGreaterEqual(len(presets), 3)
        self.assertEqual(presets[0].name, 'Home Position')


if __name__ == '__main__':
    main()
