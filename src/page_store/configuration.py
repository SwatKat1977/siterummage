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

class DatabaseSettings:
    """ Settings related to the underlying database """
    #pylint: disable=too-few-public-methods

    @property
    def username(self):
        return self._username

    @property
    def database(self):
        return self._database

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def pool_name(self):
        return self._pool_name

    @property
    def pool_size(self):
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

    @property
    def db_settings(self):
        return self._db_settings

    def __init__(self, db_config):
        self._db_settings = db_config
