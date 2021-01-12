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
from common.mysql_connector.mysql_adaptor import MySQLAdaptor
from common.service_base import ServiceBase
from .version import VERSION
from .api.health import ApiHealth
from .api.webpage import ApiWebpage

class DatabaseSettings:
    """ Settings related to the underlying database """
    #pylint: disable=too-few-public-methods

    def __init__(self, username, database, host, port, pool_name, pool_size):
        #pylint: disable=too-many-arguments
        self.username = username
        self.database = database
        self.host = host
        self.port = port
        self.pool_name = pool_name
        self.pool_size = pool_size

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

        self._db_settings = DatabaseSettings('root', 'siterummage',
                                             '127.0.0.1', 4000,
                                             'connection_pool', 1)

        self._db_adaptor = MySQLAdaptor(self._db_settings.username,
                                        self._db_settings.database,
                                        self._db_settings.host,
                                        self._db_settings.port,
                                        self._db_settings.pool_name,
                                        self._db_settings.pool_size)

        self._api_health = ApiHealth(self._quart)
        self._api_links = ApiWebpage(self._quart)

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info,
                         f'{self.title_text} {VERSION} (Core Version {CORE_VERSION})')
        self._logger.log(LogType.Info, self.copyright_text)
        self._logger.log(LogType.Info, self.license_text)

        self._is_initialised = True

        if not self._database_connection_valid():
            return False

        return True

    def _database_connection_valid(self) -> True:
        retries = 30

        self._logger.log(LogType.Info, f'MySQL host is : {self._db_settings.host}')

        while retries != 0:
            try:
                self._logger.log(LogType.Info, f'Try : {retries}')
                test_connection = self._db_adaptor.connect("master_2021")
                test_connection.close()
                self._logger.log(LogType.Info, 'Connection to database verified...')
                return True

            except RuntimeError as caught_exception:

                if str(caught_exception) == 'Incorrect user name or password':
                    self._logger.log(LogType.Error,
                                    'Invalid usernane or password for the ' \
                                    'database, failed connect to the database')
                    test_connection.close()
                    return False

                if str(caught_exception) == 'Database does not exist':
                    self._logger.log(LogType.Error,
                                    'Database does not exist, unable to ' \
                                    'connect to the database')
                    test_connection.close()
                    return False

                if str(caught_exception) == 'Unable to connect to database server':
                    self._logger.log(LogType.Error,
                                    'Unable to contact to database, retrying...')

                retries -= 1
                sleep(10)

                # raise caught_exception

        return False

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
