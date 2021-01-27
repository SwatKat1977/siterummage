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
        toplevel_page_store_api = 'page store api'
        toplevel_processing_queue_api = 'processing queue api'
        toplevel_big_broker_api = 'api settings'

        # -- Page Store Api sub-elements --
        # ---------------------------------
        page_store_api_host = 'host'
        page_store_api_port = 'port'
        page_store_api_auth_key = 'auth key'

        # -- Processing Queue Api sub-elements --
        # ---------------------------------------
        processing_queue_api_host = 'host'
        processing_queue_api_port = 'port'
        processing_queue_api_auth_key = 'auth key'

        # -- Big Broker Api sub-elements --
        # ---------------------------------
        big_broker_api_auth_key = 'auth key'

    json_schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'page store api':
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
                    'auth key':
                    {
                        "type" : "string"
                    }
                },
                "required" : ['host', 'port', 'auth key']
            },
            'processing queue api':
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
                    'auth key':
                    {
                        "type" : "string"
                    }
                },
                "required" : ['host', 'port', 'auth key']
            },
            'api settings':
            {
                "additionalProperties" : False,
                "properties":
                {
                    'auth key':
                    {
                        "type" : "string"
                    }
                },
                "required" : ['auth key']
            }
        },
        "required" : ['api settings', 'page store api', 'processing queue api']
    }
