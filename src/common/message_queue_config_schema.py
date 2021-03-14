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
    ''' Definition of the message queue configuration file JSON Schema'''
    #pylint: disable=too-few-public-methods

    # -- Top-level json elements --
    element_connection = 'connection'
    element_queue_consumer = 'consumer queue'
    element_queue_producers = 'producer queues'
    element_exchanges = 'exchanges'

    # -- Queue Entry definition --
    queue_entry_name = 'name'
    queue_entry_is_durable = 'is durable'

    # -- Exchange Entry definition --
    exchange_entry_name = 'name'
    exchange_entry_type = 'exchange type'

    # -- Messaging Service sub-elements --
    connection_username = 'username'
    connection_password = 'password'
    connection_queue_host = 'queue host'
    connection_precondition_failed_reconnect = 'reconnect on precondition failed'

    # -- Messaging Consumer sub-elements --
    queue_consumer_queue = 'queue'

    # -- Messaging Producers sub-elements --
    queue_producers_queues = 'queues'

    schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "definitions":
        {
            "queue_entry":
            {
                "type": "object",
                "additionalProperties" : False,
                "properties":
                {
                    "additionalProperties" : False,
                    queue_entry_name:
                    {
                        "type": "string"
                    },
                    queue_entry_is_durable:
                    {
                        "type": "boolean"
                    }
                },
                "required": [queue_entry_name, queue_entry_is_durable]
            },

            "exchange_entry":
            {
                "type": "object",
                "additionalProperties" : False,
                "properties":
                {
                    "additionalProperties" : False,
                    exchange_entry_name:
                    {
                        "type": "string"
                    },
                    exchange_entry_type:
                    {
                        "type": "string"
                    }
                },
                "required": [exchange_entry_name, exchange_entry_type]
            }
        },

        "type": "object",
        "additionalProperties" : False,
        "properties":
        {
            element_connection:
            {
                "additionalProperties" : False,
                "properties":
                {
                    connection_username:
                    {
                        "type" : "string"
                    },
                    connection_password:
                    {
                        "type" : "string"
                    },

                    connection_queue_host:
                    {
                        "type" : "string"
                    },
                    connection_precondition_failed_reconnect:
                    {
                        "type" : "boolean"
                    }
                },
                "required" : [connection_username,
                              connection_password,
                              connection_precondition_failed_reconnect,
                              connection_queue_host]
            },
            element_queue_consumer:
            {
                "additionalProperties" : False,
                "properties":
                {
                    queue_consumer_queue: { "$ref": "#/definitions/queue_entry"}
                },
                "required" : [queue_consumer_queue]
            },
            element_queue_producers:
            {
                "additionalProperties" : False,
                "properties":
                {
                    queue_producers_queues:
                    {
                        "type": "array",
                        "items": {"$ref": "#/definitions/queue_entry"},
                        "default": []
                    }
                },
                "required" : [queue_producers_queues]
            },

            element_exchanges:
            {
                "type": "array",
                "items": {"$ref": "#/definitions/exchange_entry"},
                "default": []
            }
        },
        "required" : [element_connection]
    }
