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
        toplevel_api_settings = 'api settings'
        toplevel_db_settings = 'database settings'

        # -- API Settings sub-elements --
        # --------------------------------
        api_settings_auth_key = 'auth key'

        # -- Database Settings sub-elements --
        # ------------------------------------
        db_settings_cache_size = 'cache size'
        db_settings_database_file = 'database file'
        db_settings_fail_on_no_db = "fail on no database"

    json_schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            "api settings":
            {
                "additionalProperties" : False,
                "properties":
                {
                    "auth key":
                    {
                        "type" : "string"
                    }
                },
                "required" : ["auth key"]
            },
            "database settings":
            {
                "additionalProperties" : False,
                "properties":
                {
                    "cache size":
                    {
                        "type" : "integer",
                        "minimum": 1
                    },
                    "database file":
                    {
                        "type" : "string"
                    },
                    "fail on no database":
                    {
                        "type": "boolean"
                    }
                },
                "required" : ["cache size", "database file",
                              "fail on no database"]
            }
        },
        "required" : ["api settings", "database settings"]
    }
