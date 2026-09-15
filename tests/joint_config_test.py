# -*- coding: UTF-8 -*-

'''
Module
    joint_config_test.py
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
    Unit tests for JointConfig value object.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.kinematics.joint_config import JointConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointConfig(TestCase):
    '''
        Test cases for JointConfig value object.

        It defines:

            :methods:
                | test_joint_config_creation - Tests instantiation of JointConfig.
                | test_joint_config_immutability - Tests frozen state of JointConfig.
    '''

    def test_joint_config_creation(self) -> None:
        '''Tests instantiation of JointConfig.'''
        cfg = JointConfig(
            joint_id=JointId.BASE,
            name='J0: Base (Yaw)',
            channel=0,
            min_deg=0.0,
            max_deg=180.0,
            home_deg=90.0,
            default_speed_deg_s=60.0,
            min_pulse_us=500,
            max_pulse_us=2500
        )
        self.assertEqual(cfg.joint_id, JointId.BASE)
        self.assertEqual(cfg.name, 'J0: Base (Yaw)')
        self.assertEqual(cfg.channel, 0)
        self.assertEqual(cfg.min_deg, 0.0)
        self.assertEqual(cfg.max_deg, 180.0)
        self.assertEqual(cfg.home_deg, 90.0)
        self.assertEqual(cfg.default_speed_deg_s, 60.0)
        self.assertEqual(cfg.min_pulse_us, 500)
        self.assertEqual(cfg.max_pulse_us, 2500)

    def test_joint_config_immutability(self) -> None:
        '''Tests frozen state of JointConfig.'''
        cfg = JointConfig(
            joint_id=JointId.LIFT_1,
            name='J1: Rame Levo',
            channel=1,
            min_deg=15.0,
            max_deg=165.0,
            home_deg=90.0,
            default_speed_deg_s=40.0,
            min_pulse_us=600,
            max_pulse_us=2400
        )
        with self.assertRaises(AttributeError):
            cfg.channel = 2  # type: ignore


if __name__ == '__main__':
    main()
