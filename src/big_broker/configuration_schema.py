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
from common.common_configuration_key import CommonConfigurationKey

class ConfigurationSchema:
    ''' Definition of the configuration files JSON Schema'''
    #pylint: disable=too-few-public-methods


    # -- Top-level json elements --
    element_page_store_api = 'page store api'
    element_big_broker_api = 'api settings'
    element_database_settings = 'database settings'
    element_message_service = 'message service'

    # -- Page Store Api sub-elements --
    # ---------------------------------
    page_store_api_host = 'host'
    page_store_api_port = 'port'

    # -- Database Settings sub-elements --
    # -------------------------------------
    db_settings_cache_size = 'cache size'
    db_settings_database_file = 'database file'
    db_settings_fail_on_no_database = 'fail on no database'

    schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            element_page_store_api:
            {
                "additionalProperties" : False,
                "properties":
                {
                    'host':
                    {
                        "type" : "string"
                    },
                    'port':
                    {
                        "type" : "integer",
                        "minimum": 1
                    },
                    CommonConfigurationKey.api_auth_key:
                    {
                        "type" : "string"
                    }
                },
                "required" : ['host', 'port',
                              CommonConfigurationKey.api_auth_key]
            },
            element_big_broker_api:
            {
                "additionalProperties" : False,
                "properties":
                {
                    CommonConfigurationKey.api_auth_key:
                    {
                        "type" : "string"
                    },
                    CommonConfigurationKey.public_key_filename:
                    {
                        "type" : "string"
                    },
                    CommonConfigurationKey.private_key_filename:
                    {
                        "type" : "string"
                    }
                },
                "required" : [CommonConfigurationKey.api_auth_key,
                              CommonConfigurationKey.public_key_filename,
                              CommonConfigurationKey.private_key_filename]
            },
            element_database_settings:
            {
                "additionalProperties" : False,
                "properties":
                {
                    db_settings_cache_size:
                    {
                        "type" : "integer",
                        "minimum": 1
                    },
                    db_settings_database_file:
                    {
                        "type" : "string"
                    },
                    db_settings_fail_on_no_database:
                    {
                        "type": "boolean"
                    }
                },
                "required" : [db_settings_cache_size,
                              db_settings_database_file,
                              db_settings_fail_on_no_database]
            }
        },
        "required" : [element_big_broker_api, element_page_store_api,
                      element_database_settings]
    }
