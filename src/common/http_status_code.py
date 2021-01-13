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

    # 429 − Too Many Requests
    TooManyRequests = 429

    ###################
    # 5xx server errors
    ###################

    # 500 - Internal Server Error
    InternalServerError = 500

    # 503 - Service Unavailable
    ServiceUnavailables = 503
