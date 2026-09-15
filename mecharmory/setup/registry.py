# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core components for simplification of mecharmory bundle registry.
'''

from __future__ import annotations

from mecharmory.setup.bundle import MecharmoryBundle
from mecharmory.setup.validator import MecharmoryBundleValidator
from mecharmory.setup.keys import MecharmoryBundleKeys
from mecharmory.setup.dependencies import MecharmoryBundleDependencies
from mecharmory.setup.dep_validator import MecharmoryBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryBundleRegistry:
    '''
        Encapsulates core components for simplification of mecharmory bundle.

        It defines:

            :methods:
                | create_bundle - Creates a mecharmory bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: MecharmoryBundleDependencies) -> MecharmoryBundle:
        '''
            Creates a mecharmory bundle.

            :param dependencies: The mecharmory bundle dependencies.
            :return: Mecharmory bundle.
            :exceptions:
                | ATSValueError: Dependencies or bundle invalid.
                | ATSTypeError: Dependencies or bundle type mismatch.
        '''
        MecharmoryBundleDependenciesValidator.validate(dependencies)

        bundle: MecharmoryBundle = MecharmoryBundle(
            base=dependencies.get(MecharmoryBundleKeys.DEPENDENCY_BASE) if dependencies else None,
            service=dependencies.get(MecharmoryBundleKeys.DEPENDENCY_SERVICE) if dependencies else None,
            gui=dependencies.get(MecharmoryBundleKeys.DEPENDENCY_GUI) if dependencies else None,
            cli=dependencies.get(MecharmoryBundleKeys.DEPENDENCY_CLI) if dependencies else None
        )

        MecharmoryBundleValidator.validate(bundle)
        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version.
        '''
        return __version__
