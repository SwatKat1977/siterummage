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
import mysql.connector
import mysql.connector.pooling
from mysql.connector import errorcode
from common.mysql_connector.mysql_connection import MySQLConnection

class MySQLAdaptor:
    ''' MySQL adaptor class '''
    __slots__ = ['_db_hostname', '_db_name', '_db_port', '_db_username',
                 '_first_connection', '_pool_name', '_pool_size']
    #pppylint: disable=R0903

    @property
    def user(self) -> str:
        """!@brief User to connect to the database with property (getter).
        @param self The object pointer.
        @returns username in string
        """
        return self._db_username

    @property
    def database_name(self) -> str:
        """!@brief Database name property (getter).
        @param self The object pointer.
        @returns database name in string
        """
        return self._db_name

    @property
    def hostname(self) -> str:
        """!@brief Host where MySQL server is running (getter).
        @param self The object pointer.
        @returns user password in string
        """
        return self._db_hostname

    @property
    def port(self) -> int:
        """!@brief Port that MySQL server is listening on (getter).
        @param self The object pointer.
        @returns port number
        """
        return self._db_port

    @property
    def pool_size(self) -> int:
        """!@brief Size of the connection pool (getter).
        @param self The object pointer.
        @returns Size of connection pool
        """
        return self._pool_size

    @property
    def pool_name(self) -> str:
        """!@brief Name of the connection pool (getter).
        @param self The object pointer.
        @returns Name of pool
        """
        return self._pool_name

    def __init__(self, user, db, host='localhost', port=3306,
                 pool_name='default_pool', pool_size=32):
        #pylint: disable=too-many-arguments
        self._db_hostname = host
        self._db_name = db
        self._db_port = port
        self._db_username = user
        self._pool_name = pool_name
        self._pool_size = pool_size

    def connect(self, user_password) -> MySQLConnection:
        """!@brief Connect to a MySQL server.
        @param self The object pointer.
        @returns MySQLConnection on success or RuntimeError on error.
        """
        #pylint: disable=R0913

        # MySQL configuration stored in a dictionary for later ease of use.
        db_config = {
            'host' : self._db_hostname,
            'port' : self._db_port,
            'user' : self._db_username,
            'password' : user_password,
            'database' : self._db_name,
            'connect_timeout': 1
        }

        try:
            # Create a  MySQL connection pool, after created, the request of
            # connecting MySQL could get a connection from this pool instead of
            # requesting to create a connection.
            conn = mysql.connector.connect(pool_name = self._pool_name,
                                           pool_size = self._pool_size,
                                           **db_config)

        except mysql.connector.errors.PoolError as mysql_except:
            raise RuntimeError('Connection pool exhausted') from mysql_except

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError('Incorrect user name or password') from err

            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError('Database does not exist')  from err

            if err.errno == errorcode.CR_CONN_HOST_ERROR:
                raise RuntimeError('Unable to connect to database server')  from err

            raise RuntimeError(f'Unhandled exception ({err.errno}) caught')  from err

        return MySQLConnection(conn)
