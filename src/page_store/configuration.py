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
    #pylint: disable=too-few-public-methods

    @property
    def username(self) -> str:
        """!@brief Database login username (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._username

    @property
    def database(self) -> str:
        """!@brief Database name (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._database

    @property
    def host(self) -> str:
        """!@brief Database server host name/ip address (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._host

    @property
    def port(self) -> int:
        """!@brief Network port MySQL is listening to on server (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._port

    @property
    def pool_name(self) -> str:
        """!@brief Name or connection pool (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._pool_name

    @property
    def pool_size(self) -> int:
        """!@brief Size of connection pool (min 1, max 32) (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._pool_size

    def __init__(self, username, database, host, port, pool_name, pool_size):
        #pylint: disable=too-many-arguments
        self._database = database
        self._host = host
        self._pool_name = pool_name
        self._pool_size = pool_size
        self._port = port
        self._username = username

class Configuration:
    """ Overal configuration settings """
    #pylint: disable=too-few-public-methods

    @property
    def db_settings(self) -> DatabaseSettings:
        """!@brief Database settins (Getter).
        @param self The object pointer.
        @returns DatabaseSettings.
        """
        return self._db_settings

    def __init__(self, db_config):
        self._db_settings = db_config
