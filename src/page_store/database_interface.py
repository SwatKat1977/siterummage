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
from time import sleep
from common.api_contracts.page_store import WebpageDetailsResponse
from common.logger import LogType
from common.mysql_connector.mysql_adaptor import MySQLAdaptor

class DatabaseInterface:
    """ Database functionalty abstraction class """
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

        query = "SELECT id FROM webpage WHERE url_path = %s AND domain = %s"
        query_args = (url_path, domain)
        results, err_msg = connection.query(query, query_args,
                                            keep_conn_alive=keep_alive)

        if err_msg:
            self._logger.log(LogType.Critical,
                             f"Query '{query}' caused a critical " + \
                             f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        return len(results)

    def get_table_lock(self, connection, lock_name) -> bool:
        """!@brief Attempt to get a lock for write using lock_name as the lock
                   identifier.
        @param self The object pointer.
        @param connection Database connection.
        @param lock_name Unique name of the lock.
        @returns True = lock retrieved, False = lock retrieval failed.
        """
        #pylint: disable=no-self-use

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
        #pylint: disable=no-self-use

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

        # Add core webpage entry
        ###########
        query = "INSERT INTO webpage(domain, url_path, read_successful, " + \
            "page_hash) VALUES(%s, %s, %s, %s)"
        query_args = (page_details.general_settings.domain,
                      page_details.general_settings.url_path,
                      page_details.general_settings.successfully_read,
                      page_details.general_settings.hash)
        results, err_msg = connection.query(query, query_args, commit=True,
                                            keep_conn_alive=True)
        if err_msg:
            self._logger.log(LogType.Critical,
                            f"Query '{query}' caused a critical " + \
                            f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        results, _ = connection.query('SELECT LAST_INSERT_ID() as last_id',
                                        keep_conn_alive=True)
        webpage_id = results[0]['last_id']

        # Add webpage metadata entry
        ###########
        query = "INSERT INTO webpage_metadata(webpage_id, title, abstract)" + \
            " VALUES(%s, %s, %s)"
        query_args = (webpage_id, page_details.metadata.title,
                      page_details.metadata.abstract)
        results, err_msg = connection.query(query, query_args, commit=True,
                                            keep_conn_alive=True)
        if err_msg:
            self._logger.log(LogType.Critical,
                            f"Query '{query}' caused a critical " + \
                            f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        results, _ = connection.query('SELECT LAST_INSERT_ID() as last_id',
                                        keep_conn_alive=True)

    async def get_webpage(self, connection, page_details) -> object:
        """!@brief Get a webpages details (if it exists), if it doesn't then
                   return an emptry dictionary.
        @param self The object pointer.
        @param connection Database connection.
        @param page_details Dictionary containing page details.
        @returns None.
        """

        query = "SELECT wp.last_scanned, wp.read_successful, " + \
                "wp.page_hash, md.title, md.abstract " + \
                "FROM webpage as wp LEFT JOIN webpage_metadata as md " + \
                "ON wp.id = md.webpage_id WHERE wp.domain = %s AND wp.url_path = %s"
        query_args = (page_details.domain, page_details.url_path)
        results, err_msg = connection.query(query, query_args,
                                            keep_conn_alive=True)
        if err_msg:
            self._logger.log(LogType.Critical,
                            f"Query '{query}' caused a critical " + \
                            f"error: {err_msg}")
            raise RuntimeError('Internal database error')

        if not results:
            return {}

        title = '' if not results[0]['title'] else results[0]['title']
        abstract = '' if not results[0]['abstract'] else results[0]['abstract']
        read_success = 'true' if results[0]['read_successful'] else 'false'
        last_scanned = results[0]['last_scanned'].strftime("%Y-%m-%d %H:%M:%S")
        page_hash = results[0]['page_hash']

        response = {
            WebpageDetailsResponse.Elements.title: title,
            WebpageDetailsResponse.Elements.abstract: abstract,
            WebpageDetailsResponse.Elements.read_successful: read_success,
            WebpageDetailsResponse.Elements.last_scanned: last_scanned,
            WebpageDetailsResponse.Elements.page_hash: page_hash
        }

        return response
