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
from quart import request
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.mime_type import MIMEType

HEADERKEY_AUTH = 'AuthKey'

class ApiWebpage:

    def __init__(self, interface_instance):
        self._interface = interface_instance
        self._auth_key = 'TesTKeY2021'

        # Add route : /webpage/add
        self._interface.add_url_rule('/webpage/add',
            methods = ['POST'], view_func = self._add_webpage)

        # Add route : /webpage/details
        self._interface.add_url_rule('/webpage/details',
            methods = ['GET'], view_func = self._get_webpage)

    async def _add_webpage(self):

        # Validate the request to ensure the auth key is present and valid.
        validate_return = self._validate_auth_key()
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        return self._interface.response_class(
            response = 'WIP', status = HTTPStatusCode.OK,
            mimetype = MIMEType.Text)

    async def _get_webpage(self, page):

        # Validate the request to ensure the auth key is present and valid.
        validate_return = self._validate_auth_key()
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        return self._interface.response_class(
            response = 'WIP', status = HTTPStatusCode.OK,
            mimetype = MIMEType.Text)

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
