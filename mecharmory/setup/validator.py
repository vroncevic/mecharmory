# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validator for the mecharmory bundle.
'''

from __future__ import annotations

from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype
from ats_utilities.base.setup.bundle import BaseBundle
from mecharmory.setup.bundle import MecharmoryBundle
from mecharmory.core.service.iservice import IService
from mecharmory.infrastructure.gui.igui_window import IGuiWindow
from mecharmory.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryBundleValidator:
    '''
        Validator for the mecharmory bundle.

        It defines:

            :methods:
                | validate - Validates the mecharmory bundle.
                | is_valid - Checks if the mecharmory bundle is valid.
    '''

    @classmethod
    def validate(cls, bundle: MecharmoryBundle) -> None:
        '''
            Validates the mecharmory bundle.

            :param bundle: The mecharmory bundle to be validated.
            :exceptions:
                | ATSValueError: The mecharmory bundle must be provided and have proper values.
                | ATSTypeError:  The mecharmory bundle must be an instance of MecharmoryBundle and
                |                its attributes must be instances of their respective types.
        '''
        ctx: str = 'mecharmory_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the mecharmory bundle must be provided'
        msg_bundle_istype: str = 'the mecharmory bundle must be an instance of MecharmoryBundle'
        msg_base_none: str = 'the base bundle must be provided'
        msg_service_none: str = 'the service must be provided'
        msg_gui_none: str = 'the gui must be provided'
        msg_cli_none: str = 'the cli must be provided'
        msg_base_istype: str = 'the base bundle must be an instance of BaseBundle'
        msg_service_istype: str = 'the service must be an instance of IService'
        msg_gui_istype: str = 'the gui must be an instance of IGuiWindow'
        msg_cli_istype: str = 'the cli must be an instance of ICLI'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, MecharmoryBundle, ctx, msg_bundle_istype)

        not_none(bundle.base, ctx, msg_base_none)
        not_none(bundle.service, ctx, msg_service_none)
        not_none(bundle.gui, ctx, msg_gui_none)
        not_none(bundle.cli, ctx, msg_cli_none)

        istype(bundle.base, BaseBundle, ctx, msg_base_istype)
        istype(bundle.service, IService, ctx, msg_service_istype)
        istype(bundle.gui, IGuiWindow, ctx, msg_gui_istype)
        istype(bundle.cli, ICLI, ctx, msg_cli_istype)

    @classmethod
    def is_valid(cls, bundle: MecharmoryBundle) -> bool:
        '''
            Checks if the mecharmory bundle is valid.

            :param bundle: The mecharmory bundle to be checked.
            :return: True if valid, False otherwise.
        '''
        try:
            cls.validate(bundle)
            return True
        except (ATSValueError, ATSTypeError):
            return False
