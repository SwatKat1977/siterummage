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
    element_api = 'api settings'
    element_big_broker = 'big broker api'
    element_page_store = 'page store api'
    element_processing_queue = 'processing queue api'

    schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            element_page_store:
            {
                "additionalProperties" : False,
                "properties":
                {
                    CommonConfigurationKey.api_endpoint:
                    {
                        "type" : "string"
                    },
                    CommonConfigurationKey.api_auth_key:
                    {
                        "type" : "string"
                    }
                },
                "required" : [CommonConfigurationKey.api_auth_key,
                              CommonConfigurationKey.api_endpoint]
            },
            element_big_broker:
            {
                "additionalProperties" : False,
                "properties":
                {
                    CommonConfigurationKey.api_endpoint:
                    {
                        "type" : "string"
                    },
                    CommonConfigurationKey.api_auth_key:
                    {
                        "type" : "string"
                    }
                },
                "required" : [CommonConfigurationKey.api_auth_key,
                              CommonConfigurationKey.api_endpoint]
            },
            element_processing_queue:
            {
                "additionalProperties" : False,
                "properties":
                {
                    CommonConfigurationKey.api_endpoint:
                    {
                        "type" : "string"
                    },
                    CommonConfigurationKey.api_auth_key:
                    {
                        "type" : "string"
                    }
                },
                "required" : [CommonConfigurationKey.api_auth_key,
                              CommonConfigurationKey.api_endpoint]
            },
            element_api:
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
                    }
                },
                "required" : [CommonConfigurationKey.api_auth_key,
                              CommonConfigurationKey.public_key_filename]
            }
        },
        "required" : [element_api, element_page_store, element_big_broker,
                      element_processing_queue]
    }
