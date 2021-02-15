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
from common.common_configuration_key import CommonConfigurationKey
from .configuration import ApiSettings, BigBrokerApi, Configuration, \
                           PageStoreApi, ProcessingQueueApi
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

    def parse_config_file(self, filename) -> Union[Configuration,None]:
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
            jsonschema.validate(instance=raw_json, schema=schema.schema)

        except jsonschema.exceptions.ValidationError:
            self._last_error_msg = f"Configuration file {filename} failed " + \
                "to validate against expected schema.  Please check!"
            return None

        raw_settings = raw_json[schema.element_api]
        api_settings = self._process_api_settings(raw_settings)

        raw_settings = raw_json[schema.element_big_broker]
        big_broker_settings = self._process_big_broker_settings(raw_settings)

        raw_settings = raw_json[schema.element_page_store]
        page_store_settings = self._process_page_store_settings(raw_settings)

        raw_settings = raw_json[schema.element_processing_queue]
        processing_queue_settings = self._process_processing_queue_settings(raw_settings)

        return Configuration(api_settings, big_broker_settings,
                             page_store_settings, processing_queue_settings)

    def _process_api_settings(self, settings) -> ApiSettings:
        """!@brief Parse the Big Broker Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns ApiSettings.
        """
        #pylint: disable=no-self-use

        auth_key = settings[CommonConfigurationKey.api_auth_key]
        public_key_file = settings[CommonConfigurationKey.public_key_filename]

        return ApiSettings(auth_key, public_key_file)

    def _process_big_broker_settings(self, settings) -> BigBrokerApi:
        """!@brief Process the big broker api settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns BigBrokerApi.
        """
        #pylint: disable=no-self-use

        auth_key = settings[CommonConfigurationKey.api_auth_key]
        api_endpoint = settings[CommonConfigurationKey.api_endpoint]

        return BigBrokerApi(auth_key, api_endpoint)

    def _process_page_store_settings(self, settings) -> PageStoreApi:
        """!@brief Process the page store api settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns PageStoreApi.
        """
        #pylint: disable=no-self-use

        auth_key = settings[CommonConfigurationKey.api_auth_key]
        api_endpoint = settings[CommonConfigurationKey.api_endpoint]

        return PageStoreApi(auth_key, api_endpoint)

    def _process_processing_queue_settings(self, settings) -> ProcessingQueueApi:
        """!@brief Parse the Processing Queue Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns PageStoreApiSettings.
        """
        #pylint: disable=no-self-use

        auth_key = settings[CommonConfigurationKey.api_auth_key]
        api_endpoint = settings[CommonConfigurationKey.api_endpoint]

        return ProcessingQueueApi(auth_key, api_endpoint)
