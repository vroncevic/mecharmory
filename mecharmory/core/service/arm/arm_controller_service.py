# -*- coding: UTF-8 -*-

'''
Module
    arm_controller_service.py
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
    Application service implementing business logic and kinematics coordination for Mecharmo.
'''

from __future__ import annotations

from typing import Callable

from mecharmory.core.model.kinematics.joint_id import JointId
from mecharmory.core.model.arm.iarm_model import IArmModel
from mecharmory.core.model.preset.motion_preset import MotionPreset
from mecharmory.core.service.serial.iserial_service import ISerialService
from mecharmory.core.service.arm.arm_command_formatter import ArmCommandFormatter
from mecharmory.core.service.arm.arm_telemetry_parser import ArmTelemetryParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArmControllerService:
    '''
        Coordinates model state updates and dispatches serial ASCII commands.

        It defines:

            :attributes:
                | _model - IArmModel interface containing state and bounds.
                | _serial_service - ISerialService interface for communication.
                | _telemetry_parser - ArmTelemetryParser for incoming lines.
                | _telemetry_callbacks - Callbacks invoked when telemetry updates.
            :methods:
                | __init__ - Configures model, communication bindings, and listeners.
                | is_initialized - Confirms service readiness.
                | get_model - Accesses IArmModel aggregate.
                | move_joint - Validates, clamps, and commands single joint angle.
                | move_all - Commands full 6-axis posture synchronously.
                | set_speed - Adjusts velocity limit for given joint.
                | stop - Commands emergency stop.
                | home - Dispatches home positioning.
                | apply_preset - Dispatches preset posture angles.
                | query_status - Queries current status from device.
                | register_telemetry_callback - Binds UI update notification.
    '''

    _model: IArmModel
    _serial_service: ISerialService
    _telemetry_parser: ArmTelemetryParser
    _telemetry_callbacks: list[Callable[[], None]]

    def __init__(self, model: IArmModel, serial_service: ISerialService) -> None:
        '''
            Initializes arm controller service.

            :param model: Domain IArmModel interface.
            :param serial_service: ISerialService interface.
        '''
        self._model = model
        self._serial_service = serial_service
        self._telemetry_parser = ArmTelemetryParser()
        self._telemetry_callbacks = []
        self._serial_service.register_rx_callback(self._on_serial_rx)

    def is_initialized(self) -> bool:
        '''
            Confirms operational readiness of arm controller.

            :return: True if model and serial service are valid.
        '''
        return self._model is not None and self._serial_service is not None

    def get_model(self) -> IArmModel:
        '''
            Returns arm model aggregate.

            :return: IArmModel instance.
        '''
        return self._model

    def move_joint(self, joint_id: JointId, target_deg: float) -> bool:
        '''
            Validates and commands single joint angle.

            :param joint_id: Joint enum index.
            :param target_deg: Desired angle.
            :return: True if command dispatched.
        '''
        clamped: float = self._model.update_target(joint_id, target_deg)
        cmd: str = ArmCommandFormatter.format_set(joint_id, clamped)
        return self._serial_service.send_line(cmd)

    def move_all(self, angles: tuple[float, ...]) -> bool:
        '''
            Commands all 6 joints simultaneously.

            :param angles: Tuple of 6 angle floats.
            :return: True if command dispatched.
        '''
        if len(angles) != 6:
            return False

        clamped_angles: list[float] = []
        for i in range(6):
            jid = JointId(i)
            c: float = self._model.update_target(jid, angles[i])
            clamped_angles.append(c)

        cmd: str = ArmCommandFormatter.format_setp(clamped_angles)
        return self._serial_service.send_line(cmd)

    def set_speed(self, joint_id: JointId, speed_deg_s: float) -> bool:
        '''
            Sets speed limit for joint.

            :param joint_id: Joint enum index.
            :param speed_deg_s: Velocity in deg/s.
            :return: True if dispatched.
        '''
        if speed_deg_s <= 0.0:
            return False

        self._model.get_state(joint_id).speed_deg_s = speed_deg_s
        cmd: str = ArmCommandFormatter.format_speed(joint_id, speed_deg_s)
        return self._serial_service.send_line(cmd)

    def stop(self) -> bool:
        '''
            Sends emergency stop command.

            :return: True if dispatched.
        '''
        for s in self._model.get_all_states():
            s.target_angle = s.current_angle
            s.is_moving = False
        return self._serial_service.send_line(ArmCommandFormatter.format_stop())

    def home(self) -> bool:
        '''
            Commands home posture for all axes.

            :return: True if dispatched.
        '''
        for s in self._model.get_all_states():
            cfg = self._model.get_config(s.joint_id)
            s.target_angle = cfg.home_deg
        return self._serial_service.send_line(ArmCommandFormatter.format_home())

    def apply_preset(self, preset: MotionPreset) -> bool:
        '''
            Applies predefined posture.

            :param preset: MotionPreset value object.
            :return: True if dispatched.
        '''
        return self.move_all(preset.angles)

    def query_status(self) -> bool:
        '''
            Requests current status frame from device.

            :return: True if request sent.
        '''
        return self._serial_service.send_line(ArmCommandFormatter.format_status())

    def register_telemetry_callback(self, callback: Callable[[], None]) -> None:
        '''
            Registers notification listener for state changes.

            :param callback: Callback function without arguments.
        '''
        self._telemetry_callbacks.append(callback)

    def _on_serial_rx(self, line: str) -> None:
        '''
            Parses status feedback from device.

            :param line: Received line.
        '''
        if self._telemetry_parser.parse(line, self._model):
            self._notify_telemetry()

    def _notify_telemetry(self) -> None:
        '''
            Dispatches UI refresh notification to registered callbacks.
        '''
        for cb in self._telemetry_callbacks:
            try:
                cb()
            except Exception:
                pass
