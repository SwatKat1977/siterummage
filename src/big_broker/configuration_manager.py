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
from .configuration import BigBrokerApiSettings, Configuration, PageStoreApi, \
                           DatabaseSettings
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
            jsonschema.validate(instance=raw_json, schema=schema.schema)

        except jsonschema.exceptions.ValidationError:
            self._last_error_msg = f"Configuration file {filename} failed " + \
                "to validate against expected schema.  Please check!"
            return None

        raw_data = raw_json[schema.element_page_store_api]
        page_store_api = self._process_page_store_api(raw_data)

        raw_data = raw_json[schema.element_big_broker_api]
        big_broker_api = self._process_big_broker_api(raw_data)

        raw_db_settings = raw_json[schema.element_database_settings]
        db_settings = self._process_db_settings(raw_db_settings)

        return Configuration(page_store_api, big_broker_api, db_settings)

    def _process_page_store_api(self, settings) -> PageStoreApi:
        """!@brief Parse the Page Store Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns PageStoreApiSettings.
        """
        #pylint: disable=no-self-use

        host = settings[schema.page_store_api_host]
        port = settings[schema.page_store_api_port]
        auth_key = settings[CommonConfigurationKey.api_auth_key]

        return PageStoreApi(host, port, auth_key)

    def _process_big_broker_api(self, settings) -> BigBrokerApiSettings:
        """!@brief Parse the Big Broker Api settings.
        @param self The object pointer.
        @param settings Raw JSON data.
        @returns BigBrokerApiSettings.
        """
        #pylint: disable=no-self-use

        auth_key = settings[CommonConfigurationKey.api_auth_key]
        private_key = settings[CommonConfigurationKey.private_key_filename]
        public_key = settings[CommonConfigurationKey.public_key_filename]

        return BigBrokerApiSettings(auth_key, private_key, public_key)

    def _process_db_settings(self, settings) -> DatabaseSettings:
        """!@brief Process the database settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns DatabaseSettings.
        """
        #pylint: disable=no-self-use

        cache_size = settings[schema.db_settings_cache_size]
        db_filename = settings[schema.db_settings_database_file]
        fail_no_db = settings[schema.db_settings_fail_on_no_database]
        return DatabaseSettings(cache_size, db_filename, fail_no_db)
