# -*- coding: UTF-8 -*-

'''
Module
    joint_id_test.py
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
    Unit tests for JointId enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.kinematics.joint_id import JointId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointId(TestCase):
    '''
        Test cases for JointId enumeration.

        It defines:

            :methods:
                | test_joint_values - Tests raw integer indices of each joint.
                | test_joint_count - Tests total number of robot joints.
                | test_joint_names - Tests enumeration identifier naming.
    '''

    def test_joint_values(self) -> None:
        '''Tests raw integer indices of each joint.'''
        self.assertEqual(JointId.BASE.value, 0)
        self.assertEqual(JointId.LIFT_1.value, 1)
        self.assertEqual(JointId.LIFT_2.value, 2)
        self.assertEqual(JointId.TUBE_ROLL.value, 3)
        self.assertEqual(JointId.END_PITCH.value, 4)
        self.assertEqual(JointId.TOOL_ROLL.value, 5)

    def test_joint_count(self) -> None:
        '''Tests total number of robot joints.'''
        self.assertEqual(len(JointId), 6)

    def test_joint_names(self) -> None:
        '''Tests enumeration identifier naming.'''
        expected = ['BASE', 'LIFT_1', 'LIFT_2', 'TUBE_ROLL', 'END_PITCH', 'TOOL_ROLL']
        actual = [j.name for j in JointId]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    main()
