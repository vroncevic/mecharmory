# -*- coding: UTF-8 -*-

'''
Module
    firmware_simulator.py
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
    Kinematic simulator maintaining virtual joint states and trajectory interpolation.
'''

from __future__ import annotations

from math import fabs
from threading import Lock

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FirmwareSimulator:
    '''
        Maintains virtual arm joint angles, speed limits, and trajectory interpolation.

        It defines:

            :attributes:
                | _lock - Thread lock guarding state transitions.
                | _current - Current angles list [J0..J5].
                | _target - Target angles list [J0..J5].
                | _speeds - Speed settings in deg/s.
                | _mins - Minimum limits in degrees.
                | _maxs - Maximum limits in degrees.
                | _homes - Home angles in degrees.
            :methods:
                | __init__ - Initializes simulated joints matching physical arm configuration.
                | home - Commands all joints to return to home positions.
                | stop - Commands all joints to stop at current positions.
                | get_angles - Returns current angles snapshot.
                | get_angle - Returns current angle for single joint index.
                | set_angle - Sets desired target angle for a single joint.
                | set_all_angles - Sets target angles for all 6 joints synchronously.
                | set_speed - Updates maximum velocity for a joint.
                | is_moving - Returns whether any joint is actively moving.
                | update_tick - Advances trajectory interpolation by elapsed delta time.
    '''

    _lock: Lock
    _current: list[float]
    _target: list[float]
    _speeds: list[float]
    _mins: list[float]
    _maxs: list[float]
    _homes: list[float]

    def __init__(self) -> None:
        '''
            Initializes simulated joints matching hardware calibration.
        '''
        self._lock = Lock()
        self._mins = [0.0, 15.0, 15.0, 0.0, 15.0, 0.0]
        self._maxs = [180.0, 165.0, 165.0, 180.0, 165.0, 180.0]
        self._homes = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
        self._speeds = [60.0, 40.0, 40.0, 70.0, 80.0, 90.0]
        self._current = list(self._homes)
        self._target = list(self._homes)

    def home(self) -> None:
        '''
            Returns all axes to their home angles.
        '''
        with self._lock:
            for i in range(6):
                self._target[i] = self._homes[i]

    def stop(self) -> None:
        '''
            Immediately arrests motion by snapping target to current angles.
        '''
        with self._lock:
            for i in range(6):
                self._target[i] = self._current[i]

    def get_angles(self) -> list[float]:
        '''
            Returns a snapshot copy of current joint angles.

            :return: List of 6 current angles in degrees.
        '''
        with self._lock:
            return list(self._current)

    def get_angle(self, index: int) -> float | None:
        '''
            Returns current angle for single joint.

            :param index: Joint index (0..5).
            :return: Current angle in degrees or None if index invalid.
        '''
        with self._lock:
            if 0 <= index < 6:
                return self._current[index]
            return None

    def set_angle(self, index: int, val: float) -> bool:
        '''
            Validates and commands single joint angle.

            :param index: Joint index (0..5).
            :param val: Commanded angle in degrees.
            :return: True if commanded within bounds.
        '''
        with self._lock:
            if not 0 <= index < 6:
                return False
            if self._mins[index] <= val <= self._maxs[index]:
                self._target[index] = val
                return True
            return False

    def set_all_angles(self, angles: list[float]) -> bool:
        '''
            Commands target angles for all 6 axes.

            :param angles: List of 6 target angles.
            :return: True if all angles are within respective physical bounds.
        '''
        if len(angles) != 6:
            return False

        with self._lock:
            for i in range(6):
                if not (self._mins[i] <= angles[i] <= self._maxs[i]):
                    return False
            for i in range(6):
                self._target[i] = angles[i]
            return True

    def set_speed(self, index: int, speed: float) -> bool:
        '''
            Adjusts speed limit for a joint.

            :param index: Joint index (0..5).
            :param speed: Commanded speed in deg/s.
            :return: True if valid positive speed.
        '''
        with self._lock:
            if 0 <= index < 6 and speed > 0.0:
                self._speeds[index] = speed
                return True
            return False

    def is_moving(self) -> bool:
        '''
            Checks whether any joint is currently transitioning towards target.

            :return: True if any joint is moving.
        '''
        with self._lock:
            return any(fabs(self._current[i] - self._target[i]) > 0.05 for i in range(6))

    def update_tick(self, dt_sec: float) -> None:
        '''
            Performs linear trajectory interpolation for all moving joints.

            :param dt_sec: Elapsed time delta in seconds.
        '''
        with self._lock:
            for i in range(6):
                diff: float = self._target[i] - self._current[i]
                if fabs(diff) < 0.01:
                    self._current[i] = self._target[i]
                    continue

                max_step: float = self._speeds[i] * dt_sec
                if fabs(diff) <= max_step:
                    self._current[i] = self._target[i]
                elif diff > 0.0:
                    self._current[i] += max_step
                else:
                    self._current[i] -= max_step
