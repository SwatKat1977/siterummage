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
from common.api_utils import ApiUtils
from common.api_contracts.scrape_node.job import NewJobTaskRequest
from common.event import Event
from common.http_status_code import HTTPStatusCode
from common.mime_type import MIMEType
from ..event_id import EventID

class ApiJob:
    __slots__ = ['_event_manager', '_logger', '_quart']

    headerkey_auth = 'AuthKey'

    def __init__(self, quart_instance, logger, event_manager):
        self._logger = logger
        self._quart = quart_instance
        self._event_manager = event_manager

        # Add route : /management/add
        self._quart.add_url_rule('/job/new_job',
            methods = ['POST'], view_func = self._new_job)

    async def _new_job(self) -> object:
 
        ### self._config.api_settings.auth_key
        auth_key = "noPassword"

        # Validate the request to ensure the auth key is present and valid.
        validate_return = ApiUtils.validate_auth_key(request,
            self.headerkey_auth, auth_key)
        if validate_return is not HTTPStatusCode.OK:
            return self._quart.response_class(
                response = 'Invalid authentication key',
                status = validate_return, mimetype = MIMEType.Text)

        obj_instance, err_msg = await ApiUtils.convert_json_body_to_object(
            request, NewJobTaskRequest.schema)

        if not obj_instance:
            return self._quart.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        check_event = Event(EventID.GetUrlBeingProcessed)
        if self._event_manager.callback_event(check_event):
            body = { 'status': 'busy' }
            return self._quart.response_class(
                response=json.dumps(body), status=HTTPStatusCode.OK,
                mimetype=MIMEType.JSON)

        message_body = {
            'url': obj_instance.url,
            'task_type': obj_instance.task_type,
            'task_id': obj_instance.task_id
        }
        new_event = Event(EventID.NewScrapeTask, message_body)
        self._event_manager.queue_event(new_event)

        body = { 'status': 'task scheduled' }
        return self._quart.response_class(
            response=json.dumps(body), status=HTTPStatusCode.OK,
            mimetype=MIMEType.JSON)
