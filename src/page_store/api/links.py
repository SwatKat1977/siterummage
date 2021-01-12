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

class ApiLinks:

    def __init__(self, interface_instance):
        self._interface = interface_instance
        self._auth_key = 'TesTKeY2021'

        # Add route : /links/add
        self._interface.add_url_rule('/links/add',
            methods = ['POST'], view_func = self._add_link)

        # Add route : /links/add
        self._interface.add_url_rule('/links/add',
            methods = ['POST'], view_func = self._add_link)

        # # Add route : /health/status
        # self._interface.add_url_rule('/health/status',
        #     methods = ['GET'], view_func = self._status)


    # async def _status(self):

    #     # Validate the request to ensure the auth key is present and valid.
    #     validate_return = self._validate_auth_key()
    #     if validate_return is not HTTPStatusCode.OK:

    #         return self._interface.response_class(
    #             response = json.dumps('Invalid authentication key'),
    #             status = validate_return, mimetype = MIMEType.Text)

    #     status_response = {
    #         'health': 'Fully Functional'
    #     }
