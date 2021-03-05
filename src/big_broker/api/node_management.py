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
from Crypto.Cipher import PKCS1_OAEP
from quart import request
import common.api_contracts.big_broker.node_management as schemas
from common.api_utils import ApiUtils
from common.http_status_code import HTTPStatusCode
from common.logger import LogType
from common.mime_type import MIMEType
from ..scrape_node_entry import ScrapeNodeEntry

class ApiNodeManagement:
    __slots__ = ['_configuration', '_cipher', '_crypto_utils', '_interface',
                 '_logger', '_private_key', '_scrape_node_list']

    header_auth_key = 'AuthKey'

    def __init__(self, interface_instance, configuration, scrape_node_list,
                 logger, crypto_utils):
        self._interface = interface_instance
        self._configuration = configuration
        self._scrape_node_list = scrape_node_list
        self._logger = logger
        self._crypto_utils = crypto_utils

        # Add route : /nodemanager/add
        self._interface.add_url_rule('/nodemanager/add',
            methods = ['POST'], view_func = self._register_scrape_node)

        # Add route : /nodemanager/list
        self._interface.add_url_rule('/nodemanager/list',
            methods = ['GET'], view_func = self._list_scrape_node)

    async def _register_scrape_node(self) -> None:
        """!@brief Implementation of the /nodemanager/add endpoint.
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
            request, schemas.NodeManagerAddRequest.schema)

        if not obj_instance:
            return self._interface.response_class(
                response=err_msg, status=HTTPStatusCode.BadRequest,
                mimetype=MIMEType.Text)

        identifier, err = self._crypto_utils.decrypt(obj_instance.identifier,
                                                     decode_base64=True)
        if not identifier:
            return self._interface.response_class(response=err,
                status=HTTPStatusCode.BadRequest, mimetype=MIMEType.Text)

        decoded_ident = identifier.decode("utf-8")

        self._logger.log(LogType.Info,
                         f"Registering node identifier {decoded_ident} " + \
                         f"from {request.remote_addr}")

        response = {
            schemas.NodeManagerAddResponse.queue_username:
                self._crypto_utils.encrypt('siterummage', True),
            schemas.NodeManagerAddResponse.queue_password:
                self._crypto_utils.encrypt('FVECLGusm4W4Psjc', True)
        }

        if self._scrape_node_list.node_exists(identifier):

            msg = f"Scrape node '{decoded_ident}' was re-registered"
            self._logger.log(LogType.Info, msg)
            return self._interface.response_class(
                response=json.dumps(response), status=HTTPStatusCode.OK,
                mimetype=MIMEType.JSON)

        node_entry = ScrapeNodeEntry(identifier)

        if not self._scrape_node_list.add_node(identifier, node_entry):
            msg = f"Scrape node '{decoded_ident}' was re-registered"
            self._logger.log(LogType.Info, msg)
            return self._interface.response_class(
                response=json.dumps(response), status=HTTPStatusCode.OK,
                mimetype=MIMEType.JSON)

        msg = f"Scrape node '{decoded_ident}' has been registered"
        self._logger.log(LogType.Info, msg)

        return self._interface.response_class(response=json.dumps(response),
                status=HTTPStatusCode.OK, mimetype=MIMEType.JSON)

    async def _list_scrape_node(self) -> None:
        """!@brief Implementation of the /nodemanager/list endpoint.
        @param self The object pointer.
        @returns None.
        """

        nodes = self._scrape_node_list.get_all_node()

        nodes_array = []
        for node in nodes.values():
            node_entry = {'identifier': node.identifier, 'host': node.host,
                          'port': node.port}
            nodes_array.append(node_entry)

        json_body = {"nodes": nodes_array}

        return self._interface.response_class(response=json.dumps(json_body),
            status=HTTPStatusCode.OK, mimetype=MIMEType.JSON)
