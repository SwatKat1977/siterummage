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
