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
from configuration import Configuration, DatabaseSettings
from configuration_schema import configurationSchema as schema

class ConfigurationManager:

    ## Property getter : Last error message
    @property
    def last_error_msg(self):
        return self._last_error_msg

    #  @param self The object pointer.
    def __init__(self):
        self._last_error_msg = ''

    #  @param self The object pointer.
    def parse_config_file(self, filename):

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

        return Configuration(db_settings)


    ## Process the central controller api settings section.
    #  @param self The object pointer.
    def _process_db_settings(self, settings):
        database = settings[schema.Elements.db_settings_database]
        host = settings[schema.Elements.db_settings_host]
        pool_name = settings[schema.Elements.db_settings_pool_name]
        pool_size = settings[schema.Elements.db_settings_pool_size]
        port = settings[schema.Elements.db_settings_port]
        username = settings[schema.Elements.db_settings_username]

        return DatabaseSettings(username, database, host, port, pool_name,
                                pool_size)
