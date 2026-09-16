# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Engine orchestrating the initialization and execution of mecharmory.
'''

from __future__ import annotations

from collections.abc import Mapping
from logging import INFO, ERROR
from sys import stdout

from ats_utilities.base.engine import Base
from ats_utilities.logger.ilogger import ILogger
from ats_utilities.exceptions import ATSValueError, ATSTypeError

from mecharmory.setup.bundle import MecharmoryBundle
from mecharmory.setup.validator import MecharmoryBundleValidator
from mecharmory.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Mecharmory(Base):
    '''
        Engine orchestrating the initialization and execution of mecharmory.

        It defines:

            :attributes:
                | _is_initialized - Flag indicating whether engine is initialized.
                | _logger - Logger for recording lifecycle and operational messages.
                | _cli - Inbound command-line interface adapter.
            :methods:
                | __init__ - Initializes the mecharmory engine with bundle.
                | process - Executes mecharmory command dispatching.
    '''

    _is_initialized: bool
    _logger: ILogger | None
    _cli: ICLI

    def __init__(self, bundle: MecharmoryBundle) -> None:
        '''
            Initializes the mecharmory engine with adapters and services.

            :param bundle: Mecharmory bundle containing adapters and services.
        '''
        self._is_initialized = False
        self._logger = None

        try:
            MecharmoryBundleValidator.validate(bundle)
            super().__init__(bundle.base)
            self._is_initialized = False
            self._cli = bundle.cli

            self._is_initialized = all(
                component.is_initialized() for component in [
                    bundle.base.option_manager,
                    bundle.service,
                    bundle.gui,
                    self._cli
                ] if component
            )

            self._logger = self.get_context().logger
            self._logger.write_log(INFO, '✅ mecharmory: engine initialized successfully!')

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ mecharmory: {exc}!\n')

        except Exception as exc:
            stdout.write(f'❌ mecharmory unexpected exception: {exc}!\n')

    def process(self, verbose: bool = False) -> bool:
        '''
            Processes the mecharmory commands.

            :param verbose: Enable verbose logging output.
            :return: True if successful, False otherwise.
        '''
        result: Mapping[str, object] = {}

        try:
            if self.is_initialized() and self._logger is not None:
                self._logger.write_log(INFO, '🔥 Starting execution command...')
                result = self._cli.run()
                self._logger.write_log(INFO, '✅ Execution finished!')

                if result.get('returncode') != 0:
                    self._logger.write_log(ERROR, f'❌ mecharmory: {result.get("stderr") or "failed!"}')
                    return False

                self._logger.write_log(INFO, '✅ mecharmory: done!')
                self._logger.write_log(INFO, '✅ mecharmory: exiting successfully!')
                return True

            if self._logger is not None:
                self._logger.write_log(ERROR, '❌ mecharmory: engine not initialized!')
            else:
                stdout.write('❌ mecharmory: engine not initialized!\n')

            return False

        except (ATSValueError, ATSTypeError) as exc:
            if self._logger is not None:
                self._logger.write_log(ERROR, f'❌ mecharmory: {exc}!')
            else:
                stdout.write(f'❌ mecharmory: {exc}!\n')

            return False

        except Exception as exc:
            if self._logger is not None:
                self._logger.write_log(ERROR, f'❌ mecharmory unexpected exception: {exc}!')
            else:
                stdout.write(f'❌ mecharmory unexpected exception: {exc}!\n')

            return False
