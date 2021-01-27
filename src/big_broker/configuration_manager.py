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
from typing import Union
import jsonschema
from .configuration import BigBrokerApiSettings, Configuration, PageStoreApi, \
                           ProcessingQueueApi
from .configuration_schema import ConfigurationSchema as schema

class ConfigurationManager:
    """ Class that manages (reads) the main JSON configuration file. """

    @property
    def last_error_msg(self):
        """!@brief Last error message (Getter).
        @param self The object pointer.
        @returns Last error message string or empty string if none.
        """
        return self._last_error_msg

    def __init__(self) -> object:
        """!@brief Class constructor.
        @param self The object pointer.
        @returns ConfigurationManager instance.
        """
        self._last_error_msg = ''

    def parse_config_file(self, filename) -> Union[Configuration, None]:
        """!@brief Parse the configuration file and then very it against the
                   JSON schema.  Once verified return an instance of the
                   Configuration class.
        @param self The object pointer.
        @param filename Filename of the configuration file to read.
        @returns Configuration if successful, otherwise on failure return None
                 and set the Last error message.
        """

        self._last_error_msg = ''

        try:
            with open(filename) as file_handle:
                file_contents = file_handle.read()

        except IOError as excpt:
            self._last_error_msg = "Unable to open configuration file '" + \
                f"{filename}', reason: {excpt.strerror}"
            return None

        try:
            raw_json = json.loads(file_contents)

        except json.JSONDecodeError as excpt:
            self._last_error_msg = "Unable to parse configuration file" + \
                f"{filename}, reason: {excpt}"
            return None

        try:
            jsonschema.validate(instance=raw_json, schema=schema.json_schema)

        except jsonschema.exceptions.ValidationError:
            self._last_error_msg = f"Configuration file {filename} failed " + \
                "to validate against expected schema.  Please check!"
            return None

        raw_data = raw_json[schema.Elements.toplevel_page_store_api]
        page_store_api = self._process_page_store_api(raw_data)

        raw_data = raw_json[schema.Elements.toplevel_processing_queue_api]
        processing_queue_api = self._process_processing_queue_api(raw_data)

        raw_data = raw_json[schema.Elements.toplevel_big_broker_api]
        big_broker_api = self._process_big_broker_api(raw_data)

        return Configuration(page_store_api, processing_queue_api,
                             big_broker_api)

    def _process_page_store_api(self, settings) -> PageStoreApi:
        """!@brief Parse the Page Store Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns PageStoreApiSettings.
        """
        #pylint: disable=no-self-use

        host = settings[schema.Elements.page_store_api_host]
        port = settings[schema.Elements.page_store_api_port]
        auth_key = settings[schema.Elements.page_store_api_auth_key]

        return PageStoreApi(host, port, auth_key)

    def _process_processing_queue_api(self, settings) -> ProcessingQueueApi:
        """!@brief Parse the Processing Queue Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns PageStoreApiSettings.
        """
        #pylint: disable=no-self-use

        host = settings[schema.Elements.processing_queue_api_host]
        port = settings[schema.Elements.processing_queue_api_port]
        auth_key = settings[schema.Elements.processing_queue_api_auth_key]

        return ProcessingQueueApi(host, port, auth_key)

    def _process_big_broker_api(self, settings) -> BigBrokerApiSettings:
        """!@brief Parse the Big Broker Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns BigBrokerApiSettings.
        """
        #pylint: disable=no-self-use

        auth_key = settings[schema.Elements.processing_queue_api_auth_key]

        return BigBrokerApiSettings(auth_key)
