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
from processing_queue.api.queue import ApiQueue
from processing_queue.db_caching.queue_cache import QueueCache
from .configuration_manager import ConfigurationManager
from .db_interface import DbInterface
from .urls_being_processed import UrlsBeingProcessed
from .version import VERSION

class Service(ServiceBase):
    """ Siterummage Processing Queue microservice class """
    #pylint: disable=too-many-instance-attributes

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Processing Queue Microservice'

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

        self._api_queue = None

        self._queue_cache = None

        self._processing_queue = None

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info,
                         f'{self.title_text} {VERSION} (Core Version {CORE_VERSION})')
        self._logger.log(LogType.Info, self.copyright_text)
        self._logger.log(LogType.Info, self.license_text)

        config_mgr = ConfigurationManager()

        config_file = os.getenv('SITERUMMAGE_PROCESSINGQUEUE_CONFIG')

        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        db_config = self._configuration.db_settings
        self._logger.log(LogType.Info, '+== Database Settings :->')
        self._logger.log(LogType.Info,
                         f'+= Cache Size          : {db_config.cache_size}')
        self._logger.log(LogType.Info,
                         f'+= DB Filename         : {db_config.database_file}')
        self._logger.log(LogType.Info,
                         f'+= Fail On No Database : {db_config.fail_on_no_database}')
        self._logger.log(LogType.Info, '+== Api Settings :->')
        self._logger.log(LogType.Info, '+= Auth Key : ******')
        self._logger.log(LogType.Info, '+==============================+')

        self._db_interface = DbInterface(db_config.database_file)

        if not self._db_interface.database_exists():
            if self._configuration.db_settings.fail_on_no_database:
                self._logger.log(LogType.Error,
                                 "DB doesn't exist and fail on create is set")
                return False

            if not self._db_interface.build_database():
                self._logger.log(LogType.Error,
                                 self._db_interface.last_error_message)
                return False

            self._logger.log(LogType.Info, 'Database created successfully')

        if not self._db_interface.open():
            self._logger.log(LogType.Error,
                             self._db_interface.last_error_message)
            return False

        self._processing_queue = UrlsBeingProcessed()

        self._queue_cache = QueueCache(self._db_interface, self._configuration,
                                       self._logger, self._processing_queue)

        self._api_queue = ApiQueue(self._quart, self._db_interface,
                                   self._configuration, self._processing_queue,
                                   self._queue_cache)

        self._is_initialised = True

        return True

    async def _main_loop(self):
        ...

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')

        if self._db_interface.is_connected:
            self._db_interface.close()
            self._logger.log(LogType.Info, '|-> Database connection closed')
