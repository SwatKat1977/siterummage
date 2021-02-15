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

class NewJobTaskRequest:
    ''' Definition of the job/new_job JSON schema'''
    #pylint: disable=too-few-public-methods

    class Elements:
        ''' Definition of the JSON elements'''
        #pylint: disable=too-few-public-methods

        url = 'url'
        task_type = 'task_type'

    schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            'url':
            {
                "type" : "string"
            },
            'task_type':
            {
                "type" : "string",
                "enum": ["new", "rescan"]
            },
            'task_id':
            {
                "type" : "string"
            }
        },
        "required" : ['url', 'task_id', 'task_type']
    }
