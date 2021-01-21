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
import jsonschema
from quart import request
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.mime_type import MIMEType
from common.api_contracts.page_store import WebpageAdd, WebpageDetails

HEADERKEY_AUTH = 'AuthKey'

class ApiWebpage:

    def __init__(self, interface_instance, db_interface, configuration):
        self._interface = interface_instance
        self._db_interface = db_interface
        self._configuration = configuration
        self._auth_key = 'TesTKeY2021'

        # Add route : /webpage/add
        self._interface.add_url_rule('/webpage/add',
            methods = ['POST'], view_func = self._add_webpage)

        # Add route : /webpage/details
        self._interface.add_url_rule('/webpage/details',
            methods = ['GET'], view_func = self._get_webpage)

    async def _add_webpage(self) -> None:
        """!@brief Implementation of the /webpage/add endpoint.
        @param self The object pointer.
        @returns None.
        """

        # Validate the request to ensure the auth key is present and valid.
        validate_return = self._validate_auth_key()
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        # Check for that the message body is of type application/json and that
        # there is one, if not report a 400 error status with a human-readable.
        body = await request.get_json()
        if not body:
            err_msg = 'Missing/invalid json body'
            response = self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)
            return response

        # Validate that the json body conforms to the expected schema.
        # If the message isn't valid then a 400 error should be generated.
        try:
            jsonschema.validate(instance=body,
                                schema=WebpageAdd.Schema)

        except jsonschema.exceptions.ValidationError:
            err_msg = 'Message body validation failed.'
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype='text')

        connection = self._db_interface.get_connection()

        if not connection:
            return self._interface.response_class(
                response='System busy',status=HTTPStatusCode.RequestTimeout,
                mimetype=MIMEType.Text)

        general_settings = body[WebpageAdd.Elements.toplevel_general]
        domain = general_settings[WebpageAdd.Elements.general_domain]
        url_path = general_settings[WebpageAdd.Elements.general_url_path]

        if self._db_interface.webpage_record_exists(connection, domain,
                                                    url_path, keep_alive=True):
            connection.close()
            return self._interface.response_class(
                response='Website and url already exists',
                status=HTTPStatusCode.NotAcceptable,
                mimetype=MIMEType.Text)

        try:
            await self._db_interface.add_webpage(connection, body)

        except RuntimeError as ex:
            connection.close()
            return self._interface.response_class(
                response = ex, status = HTTPStatusCode.OK,
                mimetype = MIMEType.Text)

        connection.close()

        return self._interface.response_class(
            response = 'Success', status = HTTPStatusCode.OK,
            mimetype = MIMEType.Text)

    async def _get_webpage(self):
        """!@brief Implementation of the /webpage/details endpoint.
        @param self The object pointer.
        @returns None.
        """

        # Validate the request to ensure the auth key is present and valid.
        validate_return = self._validate_auth_key()
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        # Check for that the message body is of type application/json and that
        # there is one, if not report a 400 error status with a human-readable.
        body = await request.get_json()
        if not body:
            err_msg = 'Missing/invalid json body'
            response = self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)
            return response

        # Validate that the json body conforms to the expected schema.
        # If the message isn't valid then a 400 error should be generated.
        try:
            jsonschema.validate(instance=body,
                                schema=WebpageDetails.Schema)

        except jsonschema.exceptions.ValidationError:
            err_msg = 'Message body validation failed.'
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype='text')

        connection = self._db_interface.get_connection()

        if not connection:
            return self._interface.response_class(
                response='System busy',status=HTTPStatusCode.RequestTimeout,
                mimetype=MIMEType.Text)

        self._db_interface.get_webpage(connection, body)

        return self._interface.response_class(
            response='Work in progress',status=HTTPStatusCode.ServiceUnavailables,
            mimetype=MIMEType.Text)

    def _validate_auth_key(self):
        """!@brief Validate the authentication key for a request.
        @param self The object pointer.
        @returns a status code:
        * 200 (OK) - Authentication key good
        * 401 (Unauthenticated) - Missing or invalid authentication key
        * 403 (Forbidden) - Invalid authentication key
        """

        # Verify that an authorisation key exists in the request header.
        if HEADERKEY_AUTH not in request.headers:
            return HTTPStatusCode.Unauthenticated

        authorisation_key = request.headers[HEADERKEY_AUTH]

        # Verify the authorisation key against what is specified in the
        # configuration file.  If it isn't valid then return 403 (Forbidden).
        if authorisation_key != self._auth_key:
            return HTTPStatusCode.Forbidden

        return HTTPStatusCode.OK
