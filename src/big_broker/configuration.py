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

class PageStoreApi:
    """ Settings related to the Page Store Api """
    __slots__ = ['_auth_key', '_host', '_port']

    @property
    def host(self) -> str:
        """!@brief Host or IP Address (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._host

    @property
    def port(self) -> str:
        """!@brief Network port the Api is listening to (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._port

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    def __init__(self, host, port, auth_key):
        #pylint: disable=too-many-arguments
        self._auth_key = auth_key
        self._host = host
        self._port = port

class BigBrokerApiSettings:
    #pylint: disable=too-few-public-methods
    """ Settings related to the Big Broker Api """
    __slots__ = ['_auth_key', '_private_key_file', '_public_key_file']

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    @property
    def private_key(self) -> str:
        """!@brief Private_key used in the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._private_key_file

    @property
    def public_key(self) -> str:
        """!@brief Public used in the Api  (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._public_key_file

    def __init__(self, auth_key, private_key_file, public_key_file):
        self._auth_key = auth_key
        self._private_key_file = private_key_file
        self._public_key_file = public_key_file

class DatabaseSettings:
    """ Settings related to the underlying database """
    __slots__ = ['_cache_size', '_database_file', '_fail_on_no_database']
    #pylint: disable=too-few-public-methods

    @property
    def cache_size(self) -> int:
        """!@brief Database default cache size (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._cache_size

    @property
    def database_file(self) -> str:
        """!@brief Database filename and path (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._database_file

    @property
    def fail_on_no_database(self) -> bool:
        """!@brief Fail on no database flag (Getter).
        @param self The object pointer.
        @returns bool.
        """
        return self._fail_on_no_database

    def __init__(self, cache_size, database_file, fail_on_no_db):
        self._cache_size = cache_size
        self._database_file = database_file
        self._fail_on_no_database = fail_on_no_db

class Configuration:
    """ Overal configuration settings """
    __slots__ = ['_big_broker_api', '_db_settings',
                 '_page_store_api', '_processing_queue_api']

    @property
    def page_store_api(self) -> PageStoreApi:
        """!@brief Page Store Api settings (Getter).
        @param self The object pointer.
        @returns PageStoreApiSettings.
        """
        return self._page_store_api

    @property
    def big_broker_api(self) -> BigBrokerApiSettings:
        """!@brief Processing Queue Api settings (Getter).
        @param self The object pointer.
        @returns ProcessingQueueApiSettings.
        """
        return self._big_broker_api

    @property
    def db_settings(self) -> DatabaseSettings:
        """!@brief Processing Queue Api settings (Getter).
        @param self The object pointer.
        @returns ProcessingQueueApiSettings.
        """
        return self._db_settings

    def __init__(self, page_store_api, big_broker_api,
                 db_settings):
        self._page_store_api = page_store_api
        self._big_broker_api = big_broker_api
        self._db_settings = db_settings
