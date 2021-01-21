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
from common.api_contracts.page_store import WebpageAdd
from common.logger import LogType
from common.mysql_connector.mysql_adaptor import MySQLAdaptor

class DatabaseInterface:
    """ Database functionalty abstraction class """
    #_pylint: disable=too-few-public-methods
    __slots__ = ['_db_adaptor', '_config', '_logger']

    domain_table_lock = 'domain_lock'

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

    def get_connection(self):
        """!@brief Get a database connection, retrying on error.
        @param self The object pointer.
        @returns MySQLConnection if a valid connection else it returns None.
        """

        tries = 1

        while tries != 10:

            try:
                return self._db_adaptor.connect('master_2021')

            except RuntimeError:
                tries += 1

            sleep(0.1)

        return None

    def webpage_record_exists(self, connection, domain, url_path,
                              keep_alive=False):
        """!@brief Check to see if a webpage record exists, it is only basic
                   data.
        @param self The object pointer.
        @param connection Database connection.
        @param domain Base domain (e.g. http://www.google.com)
        @param url_path Url after domain (e.g. /index.html)
        @param keep_alive Should connection be kept alive (default is False).
        @returns True = exists, False = doesn't exist.
        """

        domain_query = "SELECT id FROM domain WHERE name = %s"
        query_args = (domain,)
        results, err_msg = connection.query(domain_query, query_args,
                                            keep_conn_alive=keep_alive)
        if err_msg:
            self._logger.log(LogType.Critical,
                             f"Query '{domain_query}' caused a critical " + \
                             f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        if not results:
            return False

        domain_id = results[0]['id']

        url_query = "SELECT id FROM webpage WHERE name = %s AND domain_id = %s"
        query_args = (url_path, domain_id)
        results, err_msg = connection.query(url_query, query_args,
                                            keep_conn_alive=True)

        return results

    def get_table_lock(self, connection, lock_name) -> bool:
        """!@brief Attempt to get a lock for write using lock_name as the lock
                   identifier.
        @param self The object pointer.
        @param connection Database connection.
        @param lock_name Unique name of the lock.
        @returns True = lock retrieved, False = lock retrieval failed.
        """
        #_pylint: disable=no-self-use

        query = "SELECT GET_LOCK(%s,10) as 'lock'"
        query_args = (lock_name,)
        results, _ = connection.query(query, query_args,
                                      keep_conn_alive=True)
        return results[0]['lock'] == 1

    def release_table_lock(self, connection, lock_name) -> bool:
        """!@brief Release a lock using lock_name as the lock identifier.
        @param self The object pointer.
        @param connection Database connection.
        @param lock_name Unique name of the lock.
        @returns True = lock released, False = lock not released.
        """
        #_pylint: disable=no-self-use

        query = "SELECT RELEASE_LOCK(%s) as 'lock'"
        query_args = (lock_name,)
        results, _ = connection.query(query, query_args,
                                      keep_conn_alive=True)
        return results[0]['lock'] == 1

    async def add_webpage(self, connection, page_details) -> None:
        """!@brief Add webpage entries for the domain (when it does not exist),
                   webpage and its metadata.
        @param self The object pointer.
        @param connection Database connection.
        @param page_details Dictionary containing page details.
        @returns None.
        """
        #_pylint: disable=too-many-locals

        # Extract general properties from page details.
        general = page_details[WebpageAdd.Elements.toplevel_general]
        domain = general[WebpageAdd.Elements.general_domain]
        url_path = general[WebpageAdd.Elements.general_url_path]
        read_successful = general[WebpageAdd.Elements.general_read_successful]

        domain_id = None

        # Check to see if the domain exists, if it doesn't then add it.
        ###########
        domain_query = "SELECT id FROM domain WHERE name = %s"
        query_args = (domain,)
        domain_select_result, err_msg = connection.query(domain_query,
                                                         query_args,
                                                         keep_conn_alive=True)
        if err_msg:
            self._logger.log(LogType.Critical,
                             f"Query '{domain_query}' caused a critical " + \
                             f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        if not domain_select_result:
            if not self.get_table_lock(connection, self.domain_table_lock):
                raise RuntimeError('Domain table lock timeout')

            query = "INSERT INTO domain VALUES(0, %s)"
            query_args = (domain,)
            results, err_msg = connection.query(query, query_args, commit=True,
                                                keep_conn_alive=True)
            if err_msg:
                self.release_table_lock(connection, self.domain_table_lock)
                self._logger.log(LogType.Critical,
                                f"Query '{query}' caused a critical " + \
                                f"error: {err_msg}")
                raise RuntimeError('Internal database error')

            results, err_msg = connection.query('SELECT LAST_INSERT_ID() as last_id',
                                                keep_conn_alive=True)
            print(results)
            self.release_table_lock(connection, self.domain_table_lock)
            domain_id = results[0]['last_id']

        else:
            domain_id = domain_select_result[0]['id']

        # Add core webpage entry
        ###########
        query = "INSERT INTO webpage VALUES(0, %s, %s, NOW(), %s)"
        query_args = (url_path, domain_id, read_successful)
        results, err_msg = connection.query(query, query_args, commit=True,
                                            keep_conn_alive=True)
        if err_msg:
            self.release_table_lock(connection, self.domain_table_lock)
            self._logger.log(LogType.Critical,
                            f"Query '{query}' caused a critical " + \
                            f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        results, _ = connection.query('SELECT LAST_INSERT_ID() as last_id',
                                        keep_conn_alive=True)
        webpage_id = results[0]['last_id']

        # Add webpage metadata entry
        ###########
        metadata = page_details[WebpageAdd.Elements.toplevel_metadata]
        title = metadata[WebpageAdd.Elements.metadata_title]
        abstract = metadata[WebpageAdd.Elements.metadata_abstract]

        query = "INSERT INTO webpage_metadata VALUES(0, %s, %s, %s)"
        query_args = (webpage_id, title, abstract)
        results, err_msg = connection.query(query, query_args, commit=True,
                                            keep_conn_alive=True)
        if err_msg:
            self._logger.log(LogType.Critical,
                            f"Query '{query}' caused a critical " + \
                            f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        results, _ = connection.query('SELECT LAST_INSERT_ID() as last_id',
                                        keep_conn_alive=True)
