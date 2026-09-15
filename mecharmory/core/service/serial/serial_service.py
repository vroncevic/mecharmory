# -*- coding: UTF-8 -*-

'''
Module
    serial_service.py
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
    Application service managing serial worker lifecycle and dispatching communication lines.
'''

from __future__ import annotations

from typing import Callable

from mecharmory.core.service.transport.itransport import ITransport
from mecharmory.core.service.serial.serial_rx_worker import SerialRxWorker
from mecharmory.core.service.serial.serial_listener_hub import SerialListenerHub

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialService:
    '''
        Orchestrates transport stream, background worker thread, and line event handlers.

        It defines:

            :attributes:
                | _hw_transport - Hardware serial transport adapter.
                | _virt_transport - Virtual simulated transport adapter.
                | _is_virtual_mode - Boolean flag for virtual emulation.
                | _rx_worker - Background thread line reading worker.
                | _listener_hub - Callback event listener registry.
            :methods:
                | __init__ - Configures transports and state flags.
                | is_initialized - Confirms operational readiness of serial service.
                | set_virtual_mode - Toggles virtual simulation versus hardware.
                | is_virtual_mode - Returns simulation flag.
                | connect - Establishes connection on active transport.
                | disconnect - Shuts down active connection.
                | send_line - Dispatches outgoing line to active transport.
                | is_connected - Returns connection state.
                | register_rx_callback - Adds callback for received lines.
                | register_status_callback - Adds callback for connection state.
                | _on_line_received - Internal handler when worker receives line.
    '''

    _hw_transport: ITransport
    _virt_transport: ITransport
    _is_virtual_mode: bool
    _rx_worker: SerialRxWorker
    _listener_hub: SerialListenerHub

    def __init__(
        self,
        hw_transport: ITransport | None = None,
        virt_transport: ITransport | None = None
    ) -> None:
        '''
            Initializes serial service with injected transports or default adapters.

            :param hw_transport: Optional hardware transport adapter.
            :param virt_transport: Optional virtual emulation transport adapter.
            :exceptions: None.
        '''
        if hw_transport is None or virt_transport is None:
            from mecharmory.infrastructure.communication.serial_transport import SerialTransport
            from mecharmory.infrastructure.communication.virtual_serial_transport import VirtualSerialTransport
            self._hw_transport = hw_transport if hw_transport is not None else SerialTransport()
            self._virt_transport = virt_transport if virt_transport is not None else VirtualSerialTransport()
        else:
            self._hw_transport = hw_transport
            self._virt_transport = virt_transport

        self._is_virtual_mode = False
        self._rx_worker = SerialRxWorker()
        self._listener_hub = SerialListenerHub()

    def is_initialized(self) -> bool:
        '''
            Confirms operational readiness of serial service.

            :return: True if transports are properly instantiated.
            :exceptions: None.
        '''
        return self._hw_transport is not None and self._virt_transport is not None

    def set_virtual_mode(self, enabled: bool) -> None:
        '''
            Configures virtual mode.

            :param enabled: True for virtual emulator, False for real hardware.
            :exceptions: None.
        '''
        if self.is_connected():
            self.disconnect()
        self._is_virtual_mode = enabled

    def is_virtual_mode(self) -> bool:
        '''
            Returns active mode.

            :return: True if virtual, False if hardware.
            :exceptions: None.
        '''
        return self._is_virtual_mode

    def connect(self, port: str, baudrate: int) -> bool:
        '''
            Opens selected transport connection and spawns worker.

            :param port: Device path or identifier.
            :param baudrate: Baud rate speed.
            :return: True on success, False on error.
            :exceptions: None.
        '''
        self.disconnect()

        transport: ITransport = self._virt_transport if self._is_virtual_mode else self._hw_transport
        success: bool = transport.open(port, baudrate)

        if success:
            mode_desc: str = f'Connected ({"Virtual" if self._is_virtual_mode else port})'
            self._listener_hub.notify_status(True, mode_desc)
            self._rx_worker.start(transport, self._on_line_received)
        else:
            self._listener_hub.notify_status(False, f'Failed to open {port}')

        return success

    def disconnect(self) -> None:
        '''
            Terminates active connection and halts background worker.

            :exceptions: None.
        '''
        self._rx_worker.stop()
        transport: ITransport = self._virt_transport if self._is_virtual_mode else self._hw_transport
        transport.close()
        self._listener_hub.notify_status(False, 'Disconnected')

    def send_line(self, line: str) -> bool:
        '''
            Dispatches command line through active transport.

            :param line: ASCII line content.
            :return: True if successfully written.
            :exceptions: None.
        '''
        transport: ITransport = self._virt_transport if self._is_virtual_mode else self._hw_transport
        if not transport.is_open():
            return False
        return transport.write_line(line)

    def is_connected(self) -> bool:
        '''
            Checks active connection state.

            :return: True if active transport is open.
            :exceptions: None.
        '''
        transport: ITransport = self._virt_transport if self._is_virtual_mode else self._hw_transport
        return transport.is_open()

    def register_rx_callback(self, callback: Callable[[str], None]) -> None:
        '''
            Registers listener for incoming lines.

            :param callback: Handler function receiving line string.
            :exceptions: None.
        '''
        self._listener_hub.register_rx_callback(callback)

    def register_status_callback(self, callback: Callable[[bool, str], None]) -> None:
        '''
            Registers listener for connection state transitions.

            :param callback: Handler function receiving state bool and description.
            :exceptions: None.
        '''
        self._listener_hub.register_status_callback(callback)

    def _on_line_received(self, line: str) -> None:
        '''
            Internal callback triggered when rx worker reads line.

            :param line: Received ASCII line.
            :exceptions: None.
        '''
        self._listener_hub.notify_rx(line)
