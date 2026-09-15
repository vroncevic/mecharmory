# -*- coding: UTF-8 -*-

'''
Module
    joint_state_test.py
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
    Unit tests for JointState entity.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_state import JointState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointState(TestCase):
    '''
        Test cases for JointState entity.

        It defines:

            :methods:
                | test_joint_state_creation - Tests instantiation and attributes of JointState.
                | test_joint_state_mutation - Tests updating target and current angles.
    '''

    def test_joint_state_creation(self) -> None:
        '''Tests instantiation and attributes of JointState.'''
        st = JointState(
            joint_id=JointId.BASE,
            current_angle=90.0,
            target_angle=90.0,
            speed_deg_s=60.0,
            is_moving=False
        )
        self.assertEqual(st.joint_id, JointId.BASE)
        self.assertEqual(st.current_angle, 90.0)
        self.assertEqual(st.target_angle, 90.0)
        self.assertEqual(st.speed_deg_s, 60.0)
        self.assertFalse(st.is_moving)

    def test_joint_state_mutation(self) -> None:
        '''Tests updating target and current angles.'''
        st = JointState(
            joint_id=JointId.LIFT_1,
            current_angle=90.0,
            target_angle=90.0,
            speed_deg_s=40.0
        )
        st.target_angle = 120.0
        st.is_moving = True
        self.assertEqual(st.target_angle, 120.0)
        self.assertTrue(st.is_moving)
        st.current_angle = 120.0
        st.is_moving = False
        self.assertEqual(st.current_angle, 120.0)
        self.assertFalse(st.is_moving)


if __name__ == '__main__':
    main()
