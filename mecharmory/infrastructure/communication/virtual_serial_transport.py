# -*- coding: UTF-8 -*-

'''
Module
    virtual_serial_transport.py
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
    Virtual in-memory transport connected to the firmware emulator.
'''

from __future__ import annotations

from queue import Queue, Empty
from threading import Thread, Event
from time import sleep

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


class VirtualSerialTransport:
    '''
        In-memory simulated communication transport for hardware emulation.

        It defines:

            :attributes:
                | _firmware - VirtualArmFirmware simulation instance.
                | _rx_queue - Thread-safe response line queue.
                | _is_connected - State boolean.
                | _stop_event - Worker shutdown flag.
                | _sim_thread - Background 50Hz tick thread.
            :methods:
                | __init__ - Configures emulator and communication queues.
                | open - Connects to virtual firmware and starts tick loop.
                | close - Stops background tick loop cleanly.
                | write_line - Dispatches command to emulator and enqueues outputs.
                | read_line - Retrieves pending output line from emulator.
                | is_open - Queries active connectivity.
                | get_firmware - Exposes firmware instance for inspection.
    '''

    _firmware: VirtualArmFirmware
    _rx_queue: Queue[str]
    _is_connected: bool
    _stop_event: Event
    _sim_thread: Thread | None

    def __init__(self) -> None:
        '''Initializes virtual transport.'''
        self._firmware = VirtualArmFirmware()
        self._rx_queue = Queue()
        self._is_connected = False
        self._stop_event = Event()
        self._sim_thread = None

    def open(self, endpoint: str, baudrate: int) -> bool:
        '''
            Activates virtual connection and simulation thread.

            :param endpoint: Port identifier (e.g. 'VIRTUAL').
            :param baudrate: Simulated baudrate.
            :return: True always.
        '''
        self.close()
        _ = (endpoint, baudrate)
        self._stop_event.clear()
        self._is_connected = True

        # Enqueue startup banner matching physical Pico firmware
        self._rx_queue.put('===========================================')
        self._rx_queue.put(' Mecharmo 6-DOF Robotic Arm Controller v1.0.0')
        self._rx_queue.put(' Hardware: [EMULATED] Virtual Pico + PCA9685')
        self._rx_queue.put(' I2C Status: ONLINE (0x40)')
        self._rx_queue.put(' Ready for commands. Example: SET 0 90.0')
        self._rx_queue.put('===========================================')

        self._sim_thread = Thread(target=self._run_sim_loop, daemon=True)
        self._sim_thread.start()
        return True

    def close(self) -> None:
        '''Deactivates virtual connection.'''
        self._is_connected = False
        self._stop_event.set()
        if self._sim_thread is not None and self._sim_thread.is_alive():
            self._sim_thread.join(timeout=0.5)
        self._sim_thread = None

    def write_line(self, line: str) -> bool:
        '''
            Executes command on virtual firmware and collects responses.

            :param line: ASCII command string.
            :return: True if connected, False otherwise.
        '''
        if not self._is_connected:
            return False

        responses: list[str] = self._firmware.process_command(line)
        for resp in responses:
            self._rx_queue.put(resp)
        return True

    def read_line(self) -> str | None:
        '''
            Pulls next line from virtual response queue.

            :return: Decoded string or None if empty.
        '''
        if not self._is_connected:
            return None

        try:
            return self._rx_queue.get_nowait()
        except Empty:
            return None

    def is_open(self) -> bool:
        '''
            Checks connection status.

            :return: True if connected, False otherwise.
        '''
        return self._is_connected

    def get_firmware(self) -> VirtualArmFirmware:
        '''
            Returns internal firmware instance.

            :return: VirtualArmFirmware instance.
        '''
        return self._firmware

    def _run_sim_loop(self) -> None:
        '''Background loop updating simulated motion every 20ms (50Hz).'''
        while not self._stop_event.is_set():
            self._firmware.update_tick(0.020)
            sleep(0.020)
