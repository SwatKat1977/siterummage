'''
Copyright (C) 2021 Siterummage
All Rights Reserved.

NOTICE:  All information contained herein is, and remains the property of
Siterummage.  The intellectual and technical concepts contained herein are
proprietary to Siterummage and may be covered by U.K. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from Siterummage.
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
        self._api_links = ApiWebpage(self._quart)

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

        self._is_initialised = True

        return True

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
