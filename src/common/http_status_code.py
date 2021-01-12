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

    # 200 − OK
    OK = 200

    # 400 − for Bad Request
    BadRequest = 400

    # 401 − for Unauthenticated
    Unauthenticated = 401

    # 403 − for Forbidden
    Forbidden = 403

    # 404 − for Not Found
    NotFound = 404

    # 406 − for Not Acceptable
    NotAcceptable = 406

    # 415 − for Unsupported Media Type
    UnsupportedMediaType = 415

    # 429 − Too Many Requests
    TooManyRequests = 429
