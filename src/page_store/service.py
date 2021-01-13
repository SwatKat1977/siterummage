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
from time import sleep
from common.logger import Logger, LogType
from common.core_version import CORE_VERSION
from common.service_base import ServiceBase
from .api.health import ApiHealth
from .api.webpage import ApiWebpage
from .configuration import Configuration, DatabaseSettings
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

        db_settings = DatabaseSettings('root', 'siterummage',
                                        '127.0.0.1', 4000,
                                        'connection_pool', 1)
        self._configuration = Configuration(db_settings)

        self._api_health = ApiHealth(self._quart)
        self._api_links = ApiWebpage(self._quart)

        self._db_interface = DatabaseInterface(self._logger,
                                               self._configuration)

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info,
                         f'{self.title_text} {VERSION} (Core Version {CORE_VERSION})')
        self._logger.log(LogType.Info, self.copyright_text)
        self._logger.log(LogType.Info, self.license_text)

        self._is_initialised = True

        if not self._db_interface.database_connection_valid():
            return False

        return True

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
