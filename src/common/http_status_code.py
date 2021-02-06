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
# pylint: disable=too-few-public-methods

class HTTPStatusCode:
    ''' Definition of HTTP status codes '''

    #############
    # 2xx success
    #############

    # 200 − OK
    OK = 200

    # 201 - Created
    Created = 201

    # 202 - Accepted
    Accepted = 202

    # 203 - Non-Authoritative Information
    NonAuthoritativeInformation = 203

    # 204 - No Content
    NoContent = 204

    ###################
    # 4xx client errors
    ###################

    # 400 − Bad Request
    BadRequest = 400

    # 401 − Unauthenticated
    Unauthenticated = 401

    # 403 − Forbidden
    Forbidden = 403

    # 404 − Not Found
    NotFound = 404

    # 406 − Not Acceptable
    NotAcceptable = 406

    # 408 - Request Timeout
    RequestTimeout = 408

    # 415 − Unsupported Media Type
    UnsupportedMediaType = 415

    # 417 - Expectation Failed
    ExpectationFailed = 417

    # 423 - Locked
    Locked = 423

    # 429 − Too Many Requests
    TooManyRequests = 429

    ###################
    # 5xx server errors
    ###################

    # 500 - Internal Server Error
    InternalServerError = 500

    # 503 - Service Unavailable
    ServiceUnavailables = 503
