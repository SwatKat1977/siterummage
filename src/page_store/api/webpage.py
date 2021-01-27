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
from common.api_utils import ApiUtils

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
        validate_return = ApiUtils.validate_auth_key(request, HEADERKEY_AUTH,
                                                     self._auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, WebpageAdd.Schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        connection = self._db_interface.get_connection()

        if not connection:
            return self._interface.response_class(
                response='System busy',status=HTTPStatusCode.RequestTimeout,
                mimetype=MIMEType.Text)

        try:
            record_exists = self._db_interface.webpage_record_exists(
                connection, obj_instance.general_settings.domain,
                obj_instance.general_settings.url_path, keep_alive=True)

        except RuntimeError as ex:
            return self._interface.response_class(
                response = str(ex), status = HTTPStatusCode.NotAcceptable,
                mimetype = MIMEType.Text)

        if record_exists:
            connection.close()
            return self._interface.response_class(
                response='Website and url already exists',
                status=HTTPStatusCode.NotAcceptable,
                mimetype=MIMEType.Text)

        try:
            await self._db_interface.add_webpage(connection, obj_instance)

        except RuntimeError as ex:
            return self._interface.response_class(
                response = str(ex), status = HTTPStatusCode.NotAcceptable,
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
        validate_return = ApiUtils.validate_auth_key(request, HEADERKEY_AUTH,
                                                     self._auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, WebpageDetails.Schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        connection = self._db_interface.get_connection()

        if not connection:
            return self._interface.response_class(
                response='System busy',status=HTTPStatusCode.RequestTimeout,
                mimetype=MIMEType.Text)

        resp = await self._db_interface.get_webpage(connection, obj_instance)
        connection.close()

        return self._interface.response_class(
            response=json.dumps(resp),status=HTTPStatusCode.OK,
            mimetype=MIMEType.JSON)
