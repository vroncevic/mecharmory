# -*- coding: UTF-8 -*-

'''
Module
    service_engine_test.py
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
    Unit tests for composite Service orchestrator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.core.service.serial.serial_service import SerialService
from mecharmory.core.service.arm.arm_controller_service import (
    ArmControllerService
)
from mecharmory.infrastructure.storage.arm_storage_service import (
    ArmStorageService
)
from mecharmory.core.service.engine import Service

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServiceEngine(TestCase):
    '''
        Test cases for Service composite orchestrator.

        It defines:

            :attributes:
                | _context - ATS ContextBundle for test operations.
            :methods:
                | setUp - Prepares test ATS context.
                | test_service_initialization - Tests service readiness and sub-services.
                | test_subservice_getters - Tests accessing sub-services.
    '''

    _context: ContextBundle

    def setUp(self) -> None:
        '''Prepares test ATS context.'''
        self._context = ContextBundleFactory.create_bundle()

    def test_service_initialization(self) -> None:
        '''Tests service readiness and sub-services.'''
        model = ArmModel()
        serial_service = SerialService()
        arm_service = ArmControllerService(model, serial_service)
        storage = ArmStorageService(self._context)

        service = Service(arm_service, serial_service, storage)
        self.assertTrue(service.is_initialized())

    def test_subservice_getters(self) -> None:
        '''Tests accessing sub-services.'''
        model = ArmModel()
        serial_service = SerialService()
        arm_service = ArmControllerService(model, serial_service)
        storage = ArmStorageService(self._context)

        service = Service(arm_service, serial_service, storage)
        self.assertEqual(service.get_arm_service(), arm_service)
        self.assertEqual(service.get_serial_service(), serial_service)
        self.assertEqual(service.get_storage(), storage)


if __name__ == '__main__':
    main()
