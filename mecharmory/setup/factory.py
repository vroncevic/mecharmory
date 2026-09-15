# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for creating the mecharmory bundle.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from typing import Any

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from mecharmory.core.model.arm.arm_model import ArmModel
from mecharmory.core.service.serial.serial_service import SerialService
from mecharmory.core.service.arm.arm_controller_service import ArmControllerService
from mecharmory.core.service.engine import Service
from mecharmory.infrastructure.communication.serial_transport import (
    SerialTransport
)
from mecharmory.infrastructure.communication.virtual_serial_transport import (
    VirtualSerialTransport
)
from mecharmory.infrastructure.storage.arm_storage_service import (
    ArmStorageService
)
from mecharmory.infrastructure.gui.gui_window import GuiWindow
from mecharmory.infrastructure.cli.engine import CLI
from mecharmory.infrastructure.cli.setup.bundle import CLIBundle
from mecharmory.infrastructure.cli.setup.options import CLIBundleOptions
from mecharmory.infrastructure.cli.setup.factory import CLIBundleFactory
from mecharmory.setup.bundle import MecharmoryBundle
from mecharmory.setup.options import MecharmoryBundleOptions
from mecharmory.setup.registry import MecharmoryBundleRegistry
from mecharmory.setup.dependencies import MecharmoryBundleDependencies
from mecharmory.setup.opt_validator import MecharmoryBundleOptionsValidator
from mecharmory.setup.keys import MecharmoryBundleKeys
from mecharmory.setup.config_resolver import MecharmoryConfigResolver
from mecharmory.setup.model_resolver import MecharmoryModelResolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryBundleFactory:
    '''
        Factory for creating the mecharmory bundle.

        It defines:

            :attributes:
                | _info_file - Path to the mecharmory info file.
            :methods:
                | create_bundle - Creates the mecharmory bundle with optional options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'mecharmory.cfg'
    )

    @classmethod
    def create_bundle(
        cls,
        options: MecharmoryBundleOptions | None = None
    ) -> MecharmoryBundle:
        '''
            Creates the mecharmory bundle with optional pre-configured options.

            :param options: Optional pre-configured options for the bundle.
            :return: The mecharmory bundle.
            :exceptions:
                | ATSValueError: The options or dependencies must be valid.
                | ATSTypeError: The options or dependencies must match types.
        '''
        if options is not None:
            MecharmoryBundleOptionsValidator.validate(options)

        info_file: str = (
            str(options[MecharmoryBundleKeys.OPTION_INFO_FILE])
            if options and MecharmoryBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        config_data: dict[str, Any] = MecharmoryConfigResolver.resolve_config_data(
            context_bundle=context_bundle,
            options=options
        )

        model: ArmModel = MecharmoryModelResolver.resolve_model(
            config_data=config_data
        )
        storage: ArmStorageService = ArmStorageService(
            context_bundle=context_bundle
        )
        serial_service: SerialService = SerialService(
            hw_transport=SerialTransport(),
            virt_transport=VirtualSerialTransport()
        )
        arm_service: ArmControllerService = ArmControllerService(
            model=model,
            serial_service=serial_service
        )
        service: Service = Service(
            arm_service=arm_service,
            serial_service=serial_service,
            storage=storage
        )
        gui: GuiWindow = GuiWindow(
            arm_service=arm_service,
            serial_service=serial_service
        )

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui
            )
        )

        cli: CLI = CLI(cli_bundle)

        return MecharmoryBundleRegistry.create_bundle(
            dependencies=MecharmoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version string.
        '''
        return __version__
