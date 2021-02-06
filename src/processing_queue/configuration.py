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

class ApiSettings:
    """ Settings related to Processing Queue's API """
    #pylint: disable=too-few-public-methods
    __slots__ = ['_auth_key']

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    def __init__(self, auth_key):
        #pylint: disable=too-many-arguments
        self._auth_key = auth_key

class Configuration:
    """ Overal configuration settings """
    __slots__ = ['_api_settings', '_db_settings']
    #pylint: disable=too-few-public-methods

    @property
    def db_settings(self) -> DatabaseSettings:
        """!@brief Database settings (Getter).
        @param self The object pointer.
        @returns DatabaseSettings.
        """
        return self._db_settings

    @property
    def api_settings(self) -> ApiSettings:
        """!@brief Processing Queue settings (Getter).
        @param self The object pointer.
        @returns ApiSettings.
        """
        return self._api_settings

    def __init__(self, api_settings, db_config):
        self._api_settings = api_settings
        self._db_settings = db_config
