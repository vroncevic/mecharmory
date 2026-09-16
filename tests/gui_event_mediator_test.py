# -*- coding: UTF-8 -*-

'''
Module
    gui_event_mediator_test.py
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
    Unit tests for GuiEventMediator event coordination and ASCII protocol dispatching.
'''

from __future__ import annotations

from queue import Queue
from unittest import TestCase, main
from unittest.mock import MagicMock

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.infrastructure.gui.gui_event_mediator import GuiEventMediator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGuiEventMediator(TestCase):
    '''
        Test cases for GuiEventMediator coordinator.

        It defines:

            :methods:
                | setUp - Prepares mock services and queue.
                | test_constants - Verifies command constants and templates.
                | test_connect_toggle_when_disconnected - Tests connecting when disconnected.
                | test_connect_toggle_when_connected - Tests disconnecting when connected.
                | test_virtual_toggle - Tests toggling virtual emulation mode.
                | test_ping - Tests sending ping command.
                | test_joint_move - Tests commanding joint position.
                | test_tool_move - Tests commanding end tool rotation.
                | test_apply_preset - Tests applying motion preset.
                | test_home_and_stop - Tests home and stop commands.
                | test_query_status - Tests querying current arm status.
                | test_manual_command - Tests forwarding custom ASCII command.
                | test_serial_rx - Tests enqueuing received serial line.
                | test_serial_rx_filters_background_status - Tests filtering background status.
                | test_query_status_displays_response - Tests status response upon query.
                | test_manual_command_status_displays_response - Tests manual status response.
    '''

    def setUp(self) -> None:
        '''Prepares mock services and queue.'''
        self._arm_service = MagicMock()
        self._serial_service = MagicMock()
        self._ui_queue: Queue[SerialMessage] = Queue()
        self._mediator = GuiEventMediator(
            self._arm_service,
            self._serial_service,
            self._ui_queue
        )

    def test_constants(self) -> None:
        '''Verifies command constants and templates.'''
        self.assertEqual(GuiEventMediator.CMD_PING, 'PING')
        self.assertEqual(GuiEventMediator.CMD_HOME, 'HOME')
        self.assertEqual(GuiEventMediator.CMD_STOP, 'STOP')
        self.assertEqual(GuiEventMediator.CMD_STATUS, 'STATUS')
        self.assertEqual(GuiEventMediator.CMD_SET_TEMPLATE, 'SET {joint} {angle:.2f}')
        self.assertEqual(GuiEventMediator.LOG_PRESET_PREFIX, 'PRESET: ')

    def test_connect_toggle_when_disconnected(self) -> None:
        '''Tests connecting when disconnected.'''
        self._serial_service.is_connected.return_value = False
        self._mediator.on_connect_toggle('/dev/ttyUSB0', 115200)
        self._serial_service.connect.assert_called_once_with('/dev/ttyUSB0', 115200)

    def test_connect_toggle_when_connected(self) -> None:
        '''Tests disconnecting when connected.'''
        self._serial_service.is_connected.return_value = True
        self._mediator.on_connect_toggle('/dev/ttyUSB0', 115200)
        self._serial_service.disconnect.assert_called_once()

    def test_virtual_toggle(self) -> None:
        '''Tests toggling virtual emulation mode.'''
        self._mediator.on_virtual_toggle(True)
        self._serial_service.set_virtual_mode.assert_called_once_with(True)

    def test_ping(self) -> None:
        '''Tests sending ping command.'''
        self._mediator.on_ping()
        self._serial_service.send_line.assert_called_once_with('PING')
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'PING')
        self.assertEqual(msg.direction, 'TX')

    def test_joint_move(self) -> None:
        '''Tests commanding joint position.'''
        self._mediator.on_joint_move(JointId.BASE, 45.5)
        self._arm_service.move_joint.assert_called_once_with(JointId.BASE, 45.5)
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'SET 0 45.50')
        self.assertEqual(msg.direction, 'TX')

    def test_tool_move(self) -> None:
        '''Tests commanding end tool rotation.'''
        self._mediator.on_tool_move(30.0)
        self._arm_service.move_joint.assert_called_once_with(JointId.TOOL_ROLL, 30.0)
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'SET 5 30.00')
        self.assertEqual(msg.direction, 'TX')

    def test_apply_preset(self) -> None:
        '''Tests applying motion preset.'''
        preset = MotionPreset(
            name='TestPreset',
            description='Test description',
            angles=(0.0, 10.0, 20.0, 0.0, -10.0, 0.0)
        )
        self._mediator.on_apply_preset(preset)
        self._arm_service.apply_preset.assert_called_once_with(preset)
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'PRESET: TestPreset')
        self.assertEqual(msg.direction, 'TX')

    def test_home_and_stop(self) -> None:
        '''Tests home and stop commands.'''
        self._mediator.on_home()
        self._arm_service.home.assert_called_once()
        msg_home: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg_home.text, 'HOME')

        self._mediator.on_stop()
        self._arm_service.stop.assert_called_once()
        msg_stop: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg_stop.text, 'STOP')

    def test_query_status(self) -> None:
        '''Tests querying current arm status.'''
        self._mediator.on_query_status()
        self._arm_service.query_status.assert_called_once()
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'STATUS')

    def test_manual_command(self) -> None:
        '''Tests forwarding custom ASCII command.'''
        self._mediator.on_manual_command('CUSTOM_CMD 1 2 3')
        self._serial_service.send_line.assert_called_once_with('CUSTOM_CMD 1 2 3')
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'CUSTOM_CMD 1 2 3')
        self.assertEqual(msg.direction, 'TX')

    def test_serial_rx(self) -> None:
        '''Tests enqueuing received serial line.'''
        self._mediator.on_serial_rx('RX_DATA_OK')
        msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(msg.text, 'RX_DATA_OK')
        self.assertEqual(msg.direction, 'RX')

    def test_serial_rx_filters_background_status(self) -> None:
        '''Tests filtering periodic background status telemetry from console.'''
        self._mediator.on_serial_rx('STATUS J0:90.00 J1:90.00 MOVING:0')
        self.assertTrue(self._ui_queue.empty())

    def test_query_status_displays_response(self) -> None:
        '''Tests displaying status response upon explicit manual query.'''
        self._mediator.on_query_status()
        tx_msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(tx_msg.text, 'STATUS')
        self.assertEqual(tx_msg.direction, 'TX')

        self._mediator.on_serial_rx('STATUS J0:90.00 J1:90.00 MOVING:0')
        rx_msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(rx_msg.text, 'STATUS J0:90.00 J1:90.00 MOVING:0')
        self.assertEqual(rx_msg.direction, 'RX')

        # Next unsolicited status is filtered again
        self._mediator.on_serial_rx('STATUS J0:90.00 J1:90.00 MOVING:0')
        self.assertTrue(self._ui_queue.empty())

    def test_manual_command_status_displays_response(self) -> None:
        '''Tests displaying status response upon manual ASCII command.'''
        self._mediator.on_manual_command('status')
        tx_msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(tx_msg.text, 'status')
        self.assertEqual(tx_msg.direction, 'TX')

        self._mediator.on_serial_rx('STATUS J0:90.00 J1:90.00 MOVING:0')
        rx_msg: SerialMessage = self._ui_queue.get_nowait()
        self.assertEqual(rx_msg.text, 'STATUS J0:90.00 J1:90.00 MOVING:0')
        self.assertEqual(rx_msg.direction, 'RX')


if __name__ == '__main__':
    main()
