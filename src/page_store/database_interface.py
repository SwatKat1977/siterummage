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
from common.logger import LogType
from common.mysql_connector.mysql_adaptor import MySQLAdaptor

class DatabaseInterface:
    """ Database functionalty abstraction class """
    #_pylint: disable=too-few-public-methods
    __slots__ = ['_db_adaptor', '_config', '_logger']

    def __init__(self, logger, configuration):
        """!@brief DatabaseInterface class constructor
        @param self The object pointer.
        @param logger Instance of Logger class.
        @param configuration Configuration options.
        @returns Instance of DatabaseInterface class.
        """

        self._config = configuration
        self._logger = logger

        self._db_adaptor = MySQLAdaptor(self._config._db_settings.username,
                                        self._config._db_settings.database,
                                        self._config._db_settings.host,
                                        self._config._db_settings.port,
                                        self._config._db_settings.pool_name,
                                        self._config._db_settings.pool_size)

    def database_connection_valid(self) -> bool:
        """!@brief Check if the database connection is valid
        @param self The object pointer.
        @returns True = valid, False = invalid.
        """
        retries = 30

        test_connection = None
        while retries != 0:
            try:
                self._logger.log(LogType.Info,
                                 f'Connecting to database, try : {retries}')
                test_connection = self._db_adaptor.connect("master_2021")
                test_connection.close()
                self._logger.log(LogType.Info, 'Connection to database verified...')
                return True

            except RuntimeError as caught_exception:

                if str(caught_exception) == 'Incorrect user name or password':
                    self._logger.log(LogType.Error,
                                    'Invalid usernane or password for the ' \
                                    'database, failed connect to the database')
                    return False

                if str(caught_exception) == 'Database does not exist':
                    self._logger.log(LogType.Error,
                                    'Database does not exist, unable to ' \
                                    'connect to the database')
                    if test_connection:
                        test_connection.close()
                    return False

                if str(caught_exception) == 'Unable to connect to database server':
                    self._logger.log(LogType.Error,
                                    'Unable to contact to database, retrying...')

                retries -= 1
                sleep(5)

        return False

    def add_webpage(self, page_details):
        pass


        """
        CREATE TABLE domain
        (
            id BIGINT AUTO_INCREMENT,
            name VARCHAR(300),

            PRIMARY KEY(id)
        ) DEFAULT CHARACTER SET utf8;

        CREATE TABLE webpage
        (
            id BIGINT AUTO_INCREMENT,
            name VARCHAR(5000),
            domain_id BIGINT,
            last_scanned DATETIME,
            read_successfully BOOLEAN,

            PRIMARY KEY(id),
            FOREIGN KEY(domain_id) REFERENCES domain(id)
        ) DEFAULT CHARACTER SET utf8;

        CREATE TABLE webpage_metadata
        (
            id BIGINT AUTO_INCREMENT,
            webpage_id BIGINT,
            title VARCHAR(4096),
            abstract VARCHAR(4096),

            PRIMARY KEY(id),
            FOREIGN KEY(webpage_id) REFERENCES webpage(id)
        ) DEFAULT CHARACTER SET utf8;

        """
