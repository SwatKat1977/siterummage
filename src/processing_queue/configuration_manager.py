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
from .configuration import ApiSettings, Configuration, DatabaseSettings
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
            jsonschema.validate(instance=raw_json, schema=schema.json_schema)

        except jsonschema.exceptions.ValidationError:
            self._last_error_msg = f"Configuration file {filename} failed " + \
                "to validate against expected schema.  Please check!"
            return None

        raw_db_settings = raw_json[schema.Elements.toplevel_db_settings]
        db_settings = self._process_db_settings(raw_db_settings)

        raw_api_settings = raw_json[schema.Elements.toplevel_api_settings]
        api_settings = self._process_api_settings(raw_api_settings)

        return Configuration(api_settings, db_settings)

    def _process_api_settings(self, settings) -> ApiSettings:
        """!@brief Process the api settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns ApiSettings.
        """
        #pylint: disable=no-self-use

        auth_key = settings[schema.Elements.api_settings_auth_key]
        return ApiSettings(auth_key)

    def _process_db_settings(self, settings) -> DatabaseSettings:
        """!@brief Process the database settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns DatabaseSettings.
        """
        #pylint: disable=no-self-use

        cache_size = settings[schema.Elements.db_settings_cache_size]
        db_filename = settings[schema.Elements.db_settings_database_file]
        fail_no_db = settings[schema.Elements.db_settings_fail_on_no_db]
        return DatabaseSettings(cache_size, db_filename, fail_no_db)
