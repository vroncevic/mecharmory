# -*- coding: UTF-8 -*-

'''
Module
    mecha_stream_runner.py
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
    Asynchronous executor streaming compiled Mecha DSL commands to robot serial bridge.
'''

from __future__ import annotations

from threading import Thread
from time import sleep
from typing import Callable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MechaStreamRunner:
    '''
        Asynchronous command streamer sending compiled instructions with delays.

        It defines:

            :attributes:
                | _is_running - Flag indicating active execution thread.
                | _worker - Active Thread reference or None.
            :methods:
                | start - Starts asynchronous execution of commands tuple.
                | stop - Aborts execution gracefully.
                | is_running - Queries whether execution is currently active.
    '''

    _is_running: bool
    _worker: Thread | None

    def __init__(self) -> None:
        '''Initializes stream runner in idle state.'''
        self._is_running = False
        self._worker = None

    def start(
        self,
        commands: tuple[str, ...],
        send_fn: Callable[[str], None],
        on_finish: Callable[[], None] | None = None
    ) -> None:
        '''
            Begins streaming commands on background thread.

            :param commands: Tuple of compiled ASCII command lines.
            :param send_fn: Callback transmitting command to serial bridge.
            :param on_finish: Optional callback invoked upon completion.
        '''
        if self._is_running:
            return

        self._is_running = True
        self._worker = Thread(
            target=self._run_loop,
            args=(commands, send_fn, on_finish),
            daemon=True
        )
        self._worker.start()

    def stop(self) -> None:
        '''Signals active execution thread to stop immediately.'''
        self._is_running = False

    def is_running(self) -> bool:
        '''
            Queries active execution state.

            :return: True if running, False otherwise.
        '''
        return self._is_running

    def _run_loop(
        self,
        commands: tuple[str, ...],
        send_fn: Callable[[str], None],
        on_finish: Callable[[], None] | None
    ) -> None:
        '''
            Internal worker loop dispatching commands and handling delays.

            :param commands: Sequence of commands to execute.
            :param send_fn: Transmission function.
            :param on_finish: Completion callback.
        '''
        try:
            for cmd in commands:
                if not self._is_running:
                    break

                if cmd.startswith('WAIT '):
                    parts = cmd.split()
                    if len(parts) > 1 and parts[1].isdigit():
                        ms = int(parts[1])
                        sleep(ms / 1000.0)
                else:
                    send_fn(cmd)
                    sleep(0.04)

        finally:
            self._is_running = False
            if on_finish:
                on_finish()
