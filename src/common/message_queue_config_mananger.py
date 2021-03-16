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
from common.message_queue_configuration import MessageQueueConfiguration, \
     MessagingQueueSettings, MessagingQueueConsumerSettings, \
     MessagingServiceConnectSettings, MessagingQueueProducersSettings, \
     MessagingExchangeSettings, MessagingExchangesSettings
from common.message_queue_config_schema import ConfigurationSchema as schema

class MessagingQueueConfigManager:
    """ Class that manages the message queue JSON configuration file. """
    __slots__ = ['_detailed_last_error_msg', '_last_error_msg']

    @property
    def last_error_msg(self):
        """!@brief Last error message (Getter).
        @param self The object pointer.
        @returns Last error message string or empty string if none.
        """
        return self._last_error_msg

    @property
    def detailed_last_error_msg(self):
        """!@brief Last error message (Getter).
        @param self The object pointer.
        @returns Last error message string or empty string if none.
        """
        return self._detailed_last_error_msg

    def __init__(self) -> object:
        """!@brief Class constructor.
        @param self The object pointer.
        @returns ConfigurationManager instance.
        """
        self._last_error_msg = ''
        self._detailed_last_error_msg = ''

    def parse(self, filename) -> Union[MessageQueueConfiguration, None]:
        """!@brief Parse the configuration file and then very it against the
                   JSON schema.  Once verified return an instance of the
                   Configuration class.
        @param self The object pointer.
        @param filename Filename of the configuration file to read.
        @returns Configuration if successful, otherwise on failure return None
                 and set the Last error message.
        """

        self._last_error_msg = ''
        self._detailed_last_error_msg = ''

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

        except jsonschema.exceptions.ValidationError as ex:
            self._last_error_msg = f"Configuration file {filename} failed " + \
                "to validate against expected schema.  Please check!"
            self._detailed_last_error_msg = ex
            return None

        settings = raw_json[schema.element_connection]
        connection_settings = self._process_connection(settings)

        exchanges_settings = None
        if schema.element_exchanges in raw_json:
            settings = raw_json[schema.element_exchanges]
            exchanges_settings = self._process_exchanges(settings)

            if not exchanges_settings:
                return None

        consumer_settings = None
        if schema.element_queue_consumer in raw_json:
            settings = raw_json[schema.element_queue_consumer]
            consumer_settings = self._process_consumer(settings,
                                                       exchanges_settings)

            if not consumer_settings:
                return None

        producers_settings = None
        if schema.element_queue_producers in raw_json:
            settings = raw_json[schema.element_queue_producers]
            producers_settings = self._process_producers(settings,
                                                         exchanges_settings)

            if not producers_settings:
                return None

        return MessageQueueConfiguration(connection_settings,
                                         consumer_settings,
                                         producers_settings,
                                         exchanges_settings)

    def _process_connection(self, settings) -> MessagingServiceConnectSettings:
        """!@brief Process the message service connection settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns MessagingServiceConnectSettings.
        """
        #pylint: disable=no-self-use

        host = settings[schema.connection_queue_host]
        username = settings[schema.connection_username]
        password = settings[schema.connection_password]
        return MessagingServiceConnectSettings(username, password, host)

    def _process_consumer(self, settings, exchanges) -> \
            MessagingQueueConsumerSettings:
        """!@brief Process the message service consumer queue settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns MessagingQueueConsumerSettings.
        """
        #pylint: disable=no-self-use

        queue = settings[schema.queue_consumer_queue]

        domain_binding = queue[schema.queue_entry_exchange_binding] if \
            schema.queue_entry_exchange_binding in queue else None

        name = queue[schema.queue_entry_name]

        if domain_binding and not exchanges.exists(domain_binding):
            self._last_error_msg = f"Messaging queue consumer '{name}' " + \
                f"tried to bind to a non-existant exchange {domain_binding}"
            return None

        exchange_binding = None
        exchange_routing_keys = None
        if schema.queue_entry_exchange_binding in queue:
            exchange_binding = queue[schema.queue_entry_exchange_binding]
            exchange_routing_keys = queue[schema.queue_entry_exchange_routing_keys]

        entry = MessagingQueueSettings(queue[schema.queue_entry_name],
                                       queue[schema.queue_entry_is_durable],
                                       exchange_binding, exchange_routing_keys)

        return MessagingQueueConsumerSettings(entry)

    def _process_producers(self, settings, exchanges) -> \
            MessagingQueueProducersSettings:
        """!@brief Process the message service settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns MessagingServiceSettings.
        """
        #pylint: disable=no-self-use

        producers = MessagingQueueProducersSettings()

        queues = settings[schema.queue_producers_queues]

        for queue in queues:

            domain_binding = queue[schema.queue_entry_exchange_binding] if \
                schema.queue_entry_exchange_binding in queue else None

            name = queue[schema.queue_entry_name]

            if domain_binding and not exchanges.exists(domain_binding):
                self._last_error_msg = f"Messaging queue producer '{name}'" + \
                    f" tried to bind to non-existant exchange {domain_binding}"
                return None

            exchange_binding = None
            exchange_routing_keys = None
            if schema.queue_entry_exchange_binding in queue:
                exchange_binding = queue[schema.queue_entry_exchange_binding]
                exchange_routing_keys = queue[schema.queue_entry_exchange_routing_keys]

            entry = MessagingQueueSettings(queue[schema.queue_entry_name],
                                           queue[schema.queue_entry_is_durable],
                                           exchange_binding, exchange_routing_keys)
            producers.add_queue(entry)

        return producers

    def _process_exchanges(self, settings) -> MessagingExchangeSettings:
        """!@brief Process the message exchange settings section.
        @param self The object pointer.
        @param settings Raw JSON to process.
        @returns MessagingServiceSettings.
        """
        #pylint: disable=no-self-use

        exchanges = MessagingExchangesSettings()

        duplicate = []

        for queue in settings:
            name = queue[schema.exchange_entry_name]

            if exchanges.exists(name):
                duplicate.append(name)
                continue

            entry = MessagingExchangeSettings(queue[schema.exchange_entry_name],
                                              queue[schema.exchange_entry_type])
            exchanges.add(entry)

        if duplicate:
            dupe_list = ''.join(duplicate)
            plural = 's' if len(duplicate) > 1 else ''
            self._last_error_msg = f"Duplicate message exchange{plural} " + \
                f"have been defined: {dupe_list}"
            self._detailed_last_error_msg = ''
            return None

        return exchanges
