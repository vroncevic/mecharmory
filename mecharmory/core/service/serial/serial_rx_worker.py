# -*- coding: UTF-8 -*-

'''
Module
    serial_rx_worker.py
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
    Background worker thread polling incoming lines from active transport stream.
'''

from __future__ import annotations

from threading import Thread, Event
from time import sleep
from typing import Callable

from mecharmory.core.service.transport.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialRxWorker:
    '''
        Manages background thread execution for asynchronous transport line reception.

        It defines:

            :attributes:
                | _thread - Active background polling thread instance.
                | _stop_event - Event signaling thread termination.
            :methods:
                | __init__ - Initializes thread reference and stop event.
                | start - Spawns polling daemon thread.
                | stop - Signals and terminates background thread.
                | is_running - Checks if background thread is active.
                | _run_loop - Internal line polling loop.
    '''

    _thread: Thread | None
    _stop_event: Event

    def __init__(self) -> None:
        '''
            Initializes worker state.
        '''
        self._thread = None
        self._stop_event = Event()

    def start(
        self,
        transport: ITransport,
        on_line_received: Callable[[str], None]
    ) -> None:
        '''
            Spawns background polling thread.

            :param transport: Active ITransport stream.
            :param on_line_received: Callback handler for complete lines.
        '''
        self.stop()
        self._stop_event.clear()
        self._thread = Thread(
            target=self._run_loop,
            args=(transport, on_line_received),
            daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        '''
            Signals background polling to terminate.
        '''
        self._stop_event.set()
        self._thread = None

    def is_running(self) -> bool:
        '''
            Checks whether polling thread is alive.

            :return: True if active.
        '''
        return self._thread is not None and self._thread.is_alive()

    def _run_loop(
        self,
        transport: ITransport,
        on_line_received: Callable[[str], None]
    ) -> None:
        '''
            Continuously reads from transport until stop event is signaled.

            :param transport: Active ITransport stream.
            :param on_line_received: Line callback handler.
        '''
        while not self._stop_event.is_set() and transport.is_open():
            try:
                line: str | None = transport.read_line()
                if line:
                    on_line_received(line)
                else:
                    sleep(0.02)
            except Exception:
                sleep(0.05)
