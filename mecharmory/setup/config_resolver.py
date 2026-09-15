# -*- coding: UTF-8 -*-

'''
Module
    config_resolver.py
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
    Configuration resolver for mecharmory loading JSON configs and ATS schemas.
'''

from __future__ import annotations

from os.path import abspath, dirname, exists, join
from typing import Any

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys

from mecharmory.setup.options import MecharmoryBundleOptions
from mecharmory.setup.keys import MecharmoryBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://github.com/vroncevic/mecharmory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/mecharmory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MecharmoryConfigResolver:
    '''
        Configuration resolver loading and validating JSON setup using ats_utilities.

        It defines:

            :attributes:
                | _config_file - Path to default robot kinematics config file.
                | _scheme_file - Path to config schema validation file.
            :methods:
                | resolve_config_data - Loads and validates JSON configuration.
    '''

    _config_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'mecharmory_config.json'
    )
    _scheme_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'scheme.json'
    )

    @classmethod
    def resolve_config_data(
        cls,
        context_bundle: ContextBundle,
        options: MecharmoryBundleOptions | None = None
    ) -> dict[str, Any]:
        '''
            Loads and validates JSON configuration using ats_utilities.

            :param context_bundle: ATS context bundle.
            :param options: Optional bundle options.
            :return: Loaded configuration dictionary.
            :exceptions: None.
        '''
        config_path: str = (
            str(options[MecharmoryBundleKeys.OPTION_CONFIG_FILE])
            if options and MecharmoryBundleKeys.OPTION_CONFIG_FILE in options
            else cls._config_file
        )
        scheme_path: str = (
            str(options[MecharmoryBundleKeys.OPTION_SCHEME_FILE])
            if options and MecharmoryBundleKeys.OPTION_SCHEME_FILE in options
            else cls._scheme_file
        )

        if exists(config_path) and exists(scheme_path):
            try:
                scheme_bundle = ConfigIOBundleFactory.create_bundle(
                    ConfigIOBundleOptions({
                        ConfigIOBundleKeys.OPTION_FILE_PATH: scheme_path,
                        ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context_bundle
                    })
                )
                scheme = Loader(scheme_bundle).load_configuration()

                config_bundle = ConfigIOBundleFactory.create_bundle(
                    ConfigIOBundleOptions({
                        ConfigIOBundleKeys.OPTION_FILE_PATH: config_path,
                        ConfigIOBundleKeys.OPTION_SCHEME: scheme,
                        ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context_bundle
                    })
                )
                loaded = Loader(config_bundle).load_configuration()
                if isinstance(loaded, dict):
                    return loaded
            except Exception:
                pass
        return {}
