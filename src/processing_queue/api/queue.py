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
from common.mime_type import MIMEType
from common.api_contracts.processing_queue.queue import AddToQueue, \
                                                        PopFromQueue
from common.api_utils import ApiUtils

class ApiQueue:
    __slots__ = ['_db_interface', '_config', '_interface', '_processing_queue',
                 '_queue_cache']

    headerkey_auth = 'AuthKey'

    def __init__(self, interface_instance, db_interface, configuration,
                 processing_queue, queue_cache):
        self._interface = interface_instance
        self._db_interface = db_interface
        self._config = configuration
        self._processing_queue = processing_queue
        self._queue_cache = queue_cache

        # Add route : /queue/add
        self._interface.add_url_rule('/queue/add',
            methods = ['POST'], view_func = self._add_item)

        # Add route : /queue/pop
        self._interface.add_url_rule('/queue/pop',
            methods = ['GET'], view_func = self._pop_item)

    async def _add_item(self) -> object:
 
        # Validate the request to ensure the auth key is present and valid.
        validate_return = ApiUtils.validate_auth_key(request,
            self.headerkey_auth, self._config.api_settings.auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, AddToQueue.schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        return self._interface.response_class(
            response = 'Success', status = HTTPStatusCode.OK,
            mimetype = MIMEType.Text)

    async def _pop_item(self) -> object:

        # Validate the request to ensure the auth key is present and valid.
        validate_return = ApiUtils.validate_auth_key(request,
            self.headerkey_auth, self._config.api_settings.auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, PopFromQueue.schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)


        item = self._queue_cache.pop_to_processing()

        resp_json = {}

        if not item:
            return self._interface.response_class(
                response = json.dumps(resp_json), status = HTTPStatusCode.OK,
                mimetype = MIMEType.JSON)

        resp_json = {
            'url': item.url,
            'link_type': item.link_type.name
        }
        return self._interface.response_class(
            response = json.dumps(resp_json), status = HTTPStatusCode.OK,
            mimetype = MIMEType.JSON)
