# -*- coding: UTF-8 -*-

'''
Module
    virtual_arm_firmware_test.py
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
    Unit tests for VirtualArmFirmware emulator.
'''

from __future__ import annotations

from unittest import TestCase, main

from mecharmory.core.service.firmware.virtual_arm_firmware import (
    VirtualArmFirmware
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualArmFirmware(TestCase):
    '''
        Test cases for VirtualArmFirmware emulator.

        It defines:

            :methods:
                | test_empty_command - Tests ignoring empty lines.
                | test_ping_pong - Tests PING handshake command.
                | test_home_command - Tests HOME positioning command.
                | test_stop_command - Tests STOP emergency arrest command.
                | test_status_command - Tests telemetry STATUS formatting.
                | test_get_command - Tests reading single joint position.
                | test_set_command - Tests setting single joint position.
                | test_setp_command - Tests setting all joint positions.
                | test_speed_command - Tests setting joint velocity.
                | test_unknown_command - Tests reporting unknown commands.
                | test_motion_tick_interpolation - Tests kinematic tick interpolation over time.
    '''

    def test_empty_command(self) -> None:
        '''Tests ignoring empty lines.'''
        fw = VirtualArmFirmware()
        self.assertEqual(fw.process_command('   '), [])

    def test_ping_pong(self) -> None:
        '''Tests PING handshake command.'''
        fw = VirtualArmFirmware()
        self.assertEqual(fw.process_command('PING'), ['PONG'])

    def test_home_command(self) -> None:
        '''Tests HOME positioning command.'''
        fw = VirtualArmFirmware()
        self.assertEqual(fw.process_command('HOME'), ['ACK: HOME'])

    def test_stop_command(self) -> None:
        '''Tests STOP emergency arrest command.'''
        fw = VirtualArmFirmware()
        self.assertEqual(fw.process_command('STOP'), ['ACK: STOP'])

    def test_status_command(self) -> None:
        '''Tests telemetry STATUS formatting.'''
        fw = VirtualArmFirmware()
        res = fw.process_command('STATUS')
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0].startswith('STATUS J0:'))
        self.assertIn('MOVING:', res[0])

    def test_get_command(self) -> None:
        '''Tests reading single joint position.'''
        fw = VirtualArmFirmware()
        res = fw.process_command('GET 0')
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0].startswith('JOINT 0 CURRENT'))
        res_err = fw.process_command('GET 99')
        self.assertTrue(res_err[0].startswith('ERR: Unknown joint ID'))

    def test_set_command(self) -> None:
        '''Tests setting single joint position.'''
        fw = VirtualArmFirmware()
        res = fw.process_command('SET 0 45.00')
        self.assertEqual(res, ['ACK: SET 0 45.00'])
        res_err = fw.process_command('SET 8 45.00')
        self.assertTrue(res_err[0].startswith('ERR: Unknown joint ID'))

    def test_setp_command(self) -> None:
        '''Tests setting all joint positions.'''
        fw = VirtualArmFirmware()
        res = fw.process_command('SETP 45.0 50.0 60.0 70.0 80.0 90.0')
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0].startswith('ACK: SETP'))

    def test_speed_command(self) -> None:
        '''Tests setting joint velocity.'''
        fw = VirtualArmFirmware()
        res = fw.process_command('SPEED 0 50.0')
        self.assertEqual(res, ['ACK: SPEED 0 50.00'])
        res_err = fw.process_command('SPEED 0 -10.0')
        self.assertTrue(res_err[0].startswith('ERR: Invalid speed'))

    def test_unknown_command(self) -> None:
        '''Tests reporting unknown commands.'''
        fw = VirtualArmFirmware()
        self.assertEqual(fw.process_command('FOOBAR'), ['ERR: Unknown command'])

    def test_motion_tick_interpolation(self) -> None:
        '''Tests kinematic tick interpolation over time.'''
        fw = VirtualArmFirmware()
        fw.process_command('SET 0 150.00')
        self.assertTrue(fw.is_moving())
        fw.update_tick(1.0)
        angles = fw.get_angles()
        self.assertGreater(angles[0], 90.0)


if __name__ == '__main__':
    main()
