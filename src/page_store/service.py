'''
Copyright 2021 Siterummage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import os
from common.logger import Logger, LogType
from common.core_version import CORE_VERSION
from common.service_base import ServiceBase
from .api.health import ApiHealth
from .api.webpage import ApiWebpage
from .configuration_manager import ConfigurationManager
from .database_interface import DatabaseInterface
from .version import VERSION

class Service(ServiceBase):
    """ Siterummage Page Store microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Page Store Microservice'

    ## Copyright text logged on initialisation etc.
    copyright_text = 'Copyright 2021 Site Rummage'

    ## License text logged on initialisation etc.
    license_text = 'All Rights Reserved. Proprietary and confidential'

    def __init__(self, new_instance):
        super().__init__()

        self._quart = new_instance

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceThread
        self._is_initialised = False

        self._configuration = None

        self._db_interface = None

        self._api_health = ApiHealth(self._quart)
        self._api_webpage = None

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info,
                         f'{self.title_text} {VERSION} (Core Version {CORE_VERSION})')
        self._logger.log(LogType.Info, self.copyright_text)
        self._logger.log(LogType.Info, self.license_text)

        config_mgr = ConfigurationManager()

        config_file = os.getenv('SITERUMMAGE_PAGESTORE_CONFIG')

        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        db_config = self._configuration.db_settings
        self._logger.log(LogType.Info, '+== Database Settings :->')
        self._logger.log(LogType.Info, f'+= database  : {db_config.database}')
        self._logger.log(LogType.Info, f'+= host      : {db_config.host}')
        self._logger.log(LogType.Info, f'+= username  : {db_config.username}')
        self._logger.log(LogType.Info, f'+= port      : {db_config.port}')
        self._logger.log(LogType.Info, f'+= pool_name : {db_config.pool_name}')
        self._logger.log(LogType.Info, f'+= pool_size : {db_config.pool_size}')
        self._logger.log(LogType.Info, '+==============================+')

        self._db_interface = DatabaseInterface(self._logger,
                                               self._configuration)

        if not self._db_interface.database_connection_valid():
            return False

        self._api_webpage = ApiWebpage(self._quart, self._db_interface,
                                       self._configuration)

        self._is_initialised = True

        return True

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
