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
import json
from types import SimpleNamespace
import jsonschema
from common.http_status_code import HTTPStatusCode

class ApiUtils:
    """ General utilities to use with a URL """

    @staticmethod
    def validate_auth_key(request_instance, authkey_key, authkey_value):
        """!@brief Validate the authentication key for a request.
        @param self The object pointer.
        @returns a status code:
        * 200 (OK) - Authentication key good
        * 401 (Unauthenticated) - Missing or invalid authentication key
        * 403 (Forbidden) - Invalid authentication key
        """

        # Verify that an authorisation key exists in the request header.
        if authkey_key not in request_instance.headers:
            return HTTPStatusCode.Unauthenticated

        authorisation_key = request_instance.headers[authkey_key]

        # Verify the authorisation key against what is specified in the
        # configuration file.  If it isn't valid then return 403 (Forbidden).
        if authorisation_key != authkey_value:
            return HTTPStatusCode.Forbidden

        return HTTPStatusCode.OK

    @staticmethod
    async def convert_json_body_to_object(request_instance, json_schema=None):
        """!@brief Convert JSON  Validate the authentication key for a request.
        @param request_instance Instance of a message request to be converted.
        @param json_schema Optional Json schema to validate the body against.
        @returns object, error_string.  If successful then object is a valid
                 object and error_string is empty. On failure the object is
                 None and error_string is set to an appropriate error message.
        """

        # Check for that the message body is of type application/json and that
        # there is one, if not report a 400 error status with a human-readable.
        body = await request_instance.get_json()
        if not body:
            return None, 'Missing/invalid json body'

        if json_schema:
            # Validate that the json body conforms to the expected schema.  If
            # the body isn't valid then an error should be generated and object
            # returned as None.
            try:
                jsonschema.validate(instance=body, schema=json_schema)

            except jsonschema.exceptions.ValidationError:
                return None, 'Message body validation failed.'

        # Parse JSON into an object with attributes corresponding to dict keys.
        obj_instance = json.loads(await request_instance.get_data(),
                                  object_hook=lambda d: SimpleNamespace(**d))
        return obj_instance, ''
