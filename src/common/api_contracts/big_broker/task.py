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
class CompleteTaskRequest:
    ''' Definition of the task/complete_task JSON schema'''
    #pylint: disable=too-few-public-methods

    element_task_id = 'task_id'
    element_is_successful = 'is_successful'

    schema = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",

        "type" : "object",
        "additionalProperties" : False,

        "properties":
        {
            element_task_id:
            {
                "type" : "string"
            },
            element_is_successful:
            {
                "type" : "boolean",
            }
        },
        "required" : [element_task_id, element_is_successful]
    }
