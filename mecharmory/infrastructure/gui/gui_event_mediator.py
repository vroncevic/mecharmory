# -*- coding: UTF-8 -*-

'''
Module
    gui_event_mediator.py
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
    Mediator managing UI events and service dispatching across components.
'''

from __future__ import annotations

from queue import Queue

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.model.communication.serial_message import SerialMessage
from mecharmory.core.service.arm.iarm_controller_service import IArmControllerService
from mecharmory.core.service.serial.iserial_service import ISerialService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiEventMediator:
    '''
        Mediator managing UI events and dispatching to services.

        It defines:

            :attributes:
                | CMD_PING - ASCII command string for ping.
                | CMD_HOME - ASCII command string to home all axes.
                | CMD_STOP - ASCII command string for emergency stop.
                | CMD_STATUS - ASCII command string to query axis positions.
                | CMD_SET_TEMPLATE - Format string template for joint positioning command.
                | LOG_PRESET_PREFIX - Log message prefix for preset postures.
                | _arm_service - IArmControllerService instance.
                | _serial_service - ISerialService instance.
                | _ui_queue - Inter-thread event queue for UI messaging.
                | _manual_status_requests_pending - Count of explicit manual status queries.
            :methods:
                | __init__ - Initializes mediator with services and UI queue.
                | on_connect_toggle - Toggles serial connection.
                | on_virtual_toggle - Enables/disables virtual firmware mode.
                | on_ping - Sends ping command to arm controller.
                | on_joint_move - Dispatches target angle for joint.
                | on_tool_move - Dispatches tool rotation command.
                | on_apply_preset - Dispatches full arm posture preset.
                | on_home - Sends home command to arm.
                | on_stop - Sends emergency stop command to arm.
                | on_query_status - Queries current joint positions.
                | on_manual_command - Forwards manual ASCII command line.
                | on_serial_rx - Enqueues received serial line with telemetry filtering.
    '''

    CMD_PING: str = 'PING'
    CMD_HOME: str = 'HOME'
    CMD_STOP: str = 'STOP'
    CMD_STATUS: str = 'STATUS'
    CMD_SET_TEMPLATE: str = 'SET {joint} {angle:.2f}'
    LOG_PRESET_PREFIX: str = 'PRESET: '

    _arm_service: IArmControllerService
    _serial_service: ISerialService
    _ui_queue: Queue[SerialMessage]
    _manual_status_requests_pending: int

    def __init__(
        self,
        arm_service: IArmControllerService,
        serial_service: ISerialService,
        ui_queue: Queue[SerialMessage]
    ) -> None:
        '''
            Initializes mediator with dependencies.

            :param arm_service: Manipulator coordination service interface.
            :param serial_service: Communication bridge service interface.
            :param ui_queue: Thread-safe queue for UI event notifications.
        '''
        self._arm_service = arm_service
        self._serial_service = serial_service
        self._ui_queue = ui_queue
        self._manual_status_requests_pending = 0

    def on_connect_toggle(self, port: str, baud: int) -> None:
        '''Handles connect or disconnect toggle.'''
        if self._serial_service.is_connected():
            self._serial_service.disconnect()
        else:
            self._serial_service.connect(port, baud)

    def on_virtual_toggle(self, enabled: bool) -> None:
        '''Switches virtual emulation mode.'''
        self._serial_service.set_virtual_mode(enabled)

    def on_ping(self) -> None:
        '''Sends ping request.'''
        self._ui_queue.put(SerialMessage.create_tx(self.CMD_PING))
        self._serial_service.send_line(self.CMD_PING)

    def on_joint_move(self, joint_id: JointId, angle: float) -> None:
        '''Dispatches single joint movement.'''
        cmd: str = self.CMD_SET_TEMPLATE.format(joint=int(joint_id), angle=angle)
        self._ui_queue.put(SerialMessage.create_tx(cmd))
        self._arm_service.move_joint(joint_id, angle)

    def on_tool_move(self, angle: float) -> None:
        '''Dispatches tool end rotation command.'''
        self.on_joint_move(JointId.TOOL_ROLL, angle)

    def on_apply_preset(self, preset: MotionPreset) -> None:
        '''Applies posture preset.'''
        self._ui_queue.put(SerialMessage.create_tx(f'{self.LOG_PRESET_PREFIX}{preset.name}'))
        self._arm_service.apply_preset(preset)

    def on_home(self) -> None:
        '''Sends home all axes command.'''
        self._ui_queue.put(SerialMessage.create_tx(self.CMD_HOME))
        self._arm_service.home()

    def on_stop(self) -> None:
        '''Sends emergency stop command.'''
        self._ui_queue.put(SerialMessage.create_tx(self.CMD_STOP))
        self._arm_service.stop()

    def on_query_status(self) -> None:
        '''Requests status report from arm.'''
        self._manual_status_requests_pending += 1
        self._ui_queue.put(SerialMessage.create_tx(self.CMD_STATUS))
        self._arm_service.query_status()

    def on_manual_command(self, cmd_line: str) -> None:
        '''Sends raw manual ASCII command.'''
        if cmd_line.strip().upper() == self.CMD_STATUS:
            self._manual_status_requests_pending += 1

        self._ui_queue.put(SerialMessage.create_tx(cmd_line))
        self._serial_service.send_line(cmd_line)

    def on_serial_rx(self, line: str) -> None:
        '''
            Received line callback from worker thread.

            Filters out periodic background telemetry status lines from console queue,
            while permitting explicit manual status query responses.

            :param line: Received line string.
        '''
        if line.startswith(self.CMD_STATUS):
            if self._manual_status_requests_pending > 0:
                self._manual_status_requests_pending -= 1
                self._ui_queue.put(SerialMessage.create_rx(line))
        else:
            self._ui_queue.put(SerialMessage.create_rx(line))
