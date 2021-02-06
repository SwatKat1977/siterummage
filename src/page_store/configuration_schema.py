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

class ConfigurationSchema:
    ''' Definition of the configuration files JSON Schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the configuration files JSON elements'''
        #pylint: disable=too-few-public-methods

        # -- Top-level json elements --
        toplevel_db_settings = 'database settings'

        # -- Database Settings sub-elements --
        # ------------------------------------
        db_settings_database = 'database'
        db_settings_host = 'host'
        db_settings_pool_name = 'pool_name'
        db_settings_pool_size = 'pool_size'
        db_settings_port = 'port'
        db_settings_username = 'username'

    json_schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'database settings':
            {
                "additionalProperties" : False,
                "properties":
                {
                    'database':
                    {
                        "type" : "string"
                    },
                    'host':
                    {
                        "type" : "string"
                    },
                    'pool_name':
                    {
                        "type" : "string"
                    },
                    'pool_size':
                    {
                        "type" : "integer",
                        "minimum": 1,
                        "maximum": 32
                    },
                    'port':
                    {
                        "type" : "integer",
                        "minimum": 1
                    },
                    'username':
                    {
                        "type" : "string"
                    }
                },
                "required" : ['database', 'host', 'pool_name', 'pool_size',
                              'port', 'username']
            }
        },
        "required" : ['database settings']
    }
