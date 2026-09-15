# -*- coding: UTF-8 -*-

'''
Module
    arm_controller_service_test.py
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
    Unit tests for ArmControllerService application service.
'''

from __future__ import annotations

from time import sleep
from unittest import TestCase, main

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.service.serial.serial_service import SerialService
from mecharmory.core.service.arm.arm_controller_service import (
    ArmControllerService
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArmControllerService(TestCase):
    '''
        Test cases for ArmControllerService application service.

        It defines:

            :methods:
                | setUp - Configures virtual arm service stack.
                | tearDown - Cleans up active connections.
                | test_move_joint - Tests commanding a single joint.
                | test_move_all - Tests commanding all joints simultaneously.
                | test_set_speed - Tests setting joint velocity.
                | test_home_and_stop - Tests home positioning and emergency stop.
                | test_apply_preset - Tests applying motion preset.
                | test_telemetry_rx_parse - Tests parsing STATUS telemetry line.
    '''

    def setUp(self) -> None:
        '''Configures virtual arm service stack.'''
        self.model = ArmModel()
        self.serial = SerialService()
        self.serial.set_virtual_mode(True)
        self.serial.connect('VIRTUAL', 115200)
        self.controller = ArmControllerService(self.model, self.serial)

    def tearDown(self) -> None:
        '''Cleans up active connections.'''
        self.serial.disconnect()

    def test_move_joint(self) -> None:
        '''Tests commanding a single joint.'''
        sent = self.controller.move_joint(JointId.BASE, 45.0)
        self.assertTrue(sent)
        self.assertEqual(self.model.get_state(JointId.BASE).target_angle, 45.0)

    def test_move_all(self) -> None:
        '''Tests commanding all joints simultaneously.'''
        angles = (10.0, 20.0, 30.0, 40.0, 50.0, 60.0)
        sent = self.controller.move_all(angles)
        self.assertTrue(sent)
        invalid = self.controller.move_all((1.0, 2.0))
        self.assertFalse(invalid)

    def test_set_speed(self) -> None:
        '''Tests setting joint velocity.'''
        sent = self.controller.set_speed(JointId.TUBE_ROLL, 55.0)
        self.assertTrue(sent)
        self.assertEqual(self.model.get_state(JointId.TUBE_ROLL).speed_deg_s, 55.0)
        invalid = self.controller.set_speed(JointId.TUBE_ROLL, -5.0)
        self.assertFalse(invalid)

    def test_home_and_stop(self) -> None:
        '''Tests home positioning and emergency stop.'''
        self.assertTrue(self.controller.home())
        self.assertTrue(self.controller.stop())

    def test_apply_preset(self) -> None:
        '''Tests applying motion preset.'''
        preset = MotionPreset('Test', 'Desc', (90.0, 90.0, 90.0, 90.0, 90.0, 90.0))
        self.assertTrue(self.controller.apply_preset(preset))

    def test_telemetry_rx_parse(self) -> None:
        '''Tests parsing STATUS telemetry line.'''
        telemetry_notified = False

        def on_telemetry() -> None:
            nonlocal telemetry_notified
            telemetry_notified = True

        self.controller.register_telemetry_callback(on_telemetry)
        line = 'STATUS J0:45.00 J1:55.00 J2:65.00 J3:75.00 J4:85.00 J5:95.00 MOVING:1'
        self.controller._on_serial_rx(line)
        self.assertTrue(telemetry_notified)
        self.assertEqual(self.model.get_state(JointId.BASE).current_angle, 45.0)
        self.assertTrue(self.model.get_state(JointId.BASE).is_moving)


if __name__ == '__main__':
    main()
