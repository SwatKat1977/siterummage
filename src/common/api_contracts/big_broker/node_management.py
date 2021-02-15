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

class NodeManagerAddRequest:
    ''' Definition of the nodemanager/add JSON schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the JSON elements'''
        #pylint: disable=too-few-public-methods

        identifier = 'identifier'
        host = 'host'
        port = 'port'

    Schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'identifier':
            {
                "type" : "string"
            },
            'host':
            {
                "type" : "string"
            },
            'port':
            {
                "type" : "integer",
                "minimum": 1
            }
        },
        "required" : ['identifier', 'host', 'port']
    }

NodeManagerListResponseSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",

    "definitions":
    {
        'node_entry':
        {
            "type" : "object",
            "properties":
            {
                'identifier':
                {
                    "type": "string"
                },
                'host':
                {
                    "type": "string"
                },
                'port':
                {
                    "type": "integer"
                }
            },
            "additionalProperties": False,
            "required": ['identifier', 'host', 'port']
        }
    },
    "type" : "object",
    "properties":
    {
        'nodes':
        {
            "type": "array",
            "items": {"$ref": f"#/definitions/{'node_entry'}"}
        }
    },
    "required" : ['nodes'],
    "additionalProperties" : False
}
