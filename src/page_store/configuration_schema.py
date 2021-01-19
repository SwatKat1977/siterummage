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

class configurationSchema:
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
                        "type" : "integer"
                    },
                    'port':
                    {
                        "type" : "integer"
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
