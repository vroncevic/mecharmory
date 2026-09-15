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
    Composite core application service coordinating arm control, serial, and storage subsystems.
'''

from __future__ import annotations

from mecharmory.core.service.arm.iarm_controller_service import IArmControllerService
from mecharmory.core.service.serial.iserial_service import ISerialService
from mecharmory.core.service.storage.iarm_storage_service import IArmStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Service:
    '''
        Application service coordinating robotic arm kinematics, communication, and storage.

        It defines:

            :attributes:
                | _arm_service - IArmControllerService instance.
                | _serial_service - ISerialService instance.
                | _storage - IArmStorageService instance.
            :methods:
                | __init__ - Initializes the composite service with injected abstractions.
                | is_initialized - Confirms operational readiness of all sub-services.
                | get_arm_service - Returns active IArmControllerService.
                | get_serial_service - Returns active ISerialService.
                | get_storage - Returns active IArmStorageService.
    '''

    _arm_service: IArmControllerService
    _serial_service: ISerialService
    _storage: IArmStorageService

    def __init__(
        self,
        arm_service: IArmControllerService,
        serial_service: ISerialService,
        storage: IArmStorageService
    ) -> None:
        '''
            Initializes the composite service with injected abstractions.

            :param arm_service: IArmControllerService instance.
            :param serial_service: ISerialService instance.
            :param storage: IArmStorageService instance.
        '''
        self._arm_service = arm_service
        self._serial_service = serial_service
        self._storage = storage

    def is_initialized(self) -> bool:
        '''
            Confirms operational readiness of all sub-services.

            :return: True if all sub-services are initialized.
        '''
        return (
            self._arm_service is not None
            and self._arm_service.is_initialized()
            and self._serial_service is not None
            and self._serial_service.is_initialized()
            and self._storage is not None
            and self._storage.is_initialized()
        )

    def get_arm_service(self) -> IArmControllerService:
        '''
            Returns active IArmControllerService instance.

            :return: IArmControllerService instance.
        '''
        return self._arm_service

    def get_serial_service(self) -> ISerialService:
        '''
            Returns active ISerialService instance.

            :return: ISerialService instance.
        '''
        return self._serial_service

    def get_storage(self) -> IArmStorageService:
        '''
            Returns active IArmStorageService instance.

            :return: IArmStorageService instance.
        '''
        return self._storage
