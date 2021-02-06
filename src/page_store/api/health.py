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
from quart import request
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.mime_type import MIMEType

HEADERKEY_AUTH = 'AuthKey'

class ApiHealth:

    def __init__(self, interface_instance):
        self._interface = interface_instance
        self._auth_key = 'TesTKeY2021'

        # Add route : /health/ping
        self._interface.add_url_rule('/health/ping',
            methods = ['GET'], view_func = self._ping)

        # Add route : /health/status
        self._interface.add_url_rule('/health/status',
            methods = ['GET'], view_func = self._status)

    async def _ping(self):
        return self._interface.response_class(response = 'pong',
            status = HTTPStatusCode.OK, mimetype = MIMEType.Text)

    async def _status(self):

        # Validate the request to ensure the auth key is present and valid.
        validate_return = self._validate_auth_key()
        if validate_return is not HTTPStatusCode.OK:

            return self._interface.response_class(
                response = json.dumps('Invalid authentication key'),
                status = validate_return, mimetype = MIMEType.Text)

        status_response = {
            'health': 'Fully Functional'
        }

        return self._interface.response_class(
            response = json.dumps(status_response),
            status = HTTPStatusCode.OK, mimetype = MIMEType.JSON)

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
