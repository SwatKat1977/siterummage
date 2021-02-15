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
import common.api_contracts.big_broker.task as schemas
from common.api_utils import ApiUtils
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.mime_type import MIMEType

class ApiTask:
    __slots__ = ['_configuration', '_interface', '_logger']

    header_auth_key = 'AuthKey'

    def __init__(self, interface_instance, configuration, logger):
        self._interface = interface_instance
        self._configuration = configuration
        self._logger = logger

        # Add route : /task/complete_task
        self._interface.add_url_rule('/task/complete_task',
            methods = ['POST'], view_func = self._complete_task)

    async def _complete_task(self) -> None:
        """!@brief Implementation of the /task/complete_task endpoint.
        @param self The object pointer.
        @returns None.
        """

        auth_key = self._configuration.big_broker_api.auth_key

        # Validate the request to ensure the auth key is present and valid.
        validate_return = ApiUtils.validate_auth_key(request,
                                                     self.header_auth_key,
                                                     auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._interface.response_class(
                response='Invalid authentication key',
                status=validate_return, mimetype=MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, schemas.CompleteTaskRequest.schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        self._logger.log(LogType.Info, f'Task Id       : {obj_instance.task_id}')
        self._logger.log(LogType.Info, f'Is Successful : {obj_instance.is_successful}')

        return self._interface.response_class(
            response='placeholder', status=HTTPStatusCode.OK,
            mimetype=MIMEType.Text)
