'''
Copyright (C) 2021 Siterummage Development Team

'''
import mysql.connector
import mysql.connector.pooling
from mysql.connector import errorcode
from common.MySqlInterface.MySQLConnection import MySQLConnection

class MySQLAdaptor:
    ''' MySQL adaptor class '''
    #pylint: disable=R0903

    @staticmethod
    def connect(user, password, database, host='localhost', port=3306,
                pool_size=32, pool_name='mysql_pool'):
        """!@brief Connect to a MySQL server.
        @param user User to connect to the database with
        @param password Passport for connection user
        @param host Hostname or IP address of the MySQL server
        @param port Network port the Mysql server is listening on
        @param pool_size Size of the connection pool
        @param pool_name User-readable name of the connection pool
        @returns MySQLConnection on success or RuntimeError on error.
        """
        #pylint: disable=R0913

        # MySQL configuration stored in a dictionary for later ease of use.
        db_config = {
            'host' : host,
            'port' : port,
            'user' : user,
            'password' : password,
            'database' : database
        }

        try:
            # Create a  MySQL connection pool, after created, the request of
            # connecting MySQL could get a connection from this pool instead of
            # requesting to create a connection.
            connection = mysql.connector.connect(pool_name = "mypool",
                                                 pool_size = pool_size,
                                                 **db_config)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError('Incorrect user name or password') from err

            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError('Database does not exist')  from err

            return(None, err)

        return MySQLConnection(connection, pool_name, pool_size)
