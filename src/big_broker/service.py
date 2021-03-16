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
from operator import itemgetter
import os
from common.crypto_utils import CryptoUtils
from common.logger import Logger, LogType
from common.info import BUILD_NO, COPYRIGHT_TEXT, CORE_VERSION, LICENSE_TEXT
from common.message_queue_config_mananger import MessagingQueueConfigManager
from common.messaging_queue_settings import ExchangeEntry, \
                                            MessagingQueueSettings, QueueEntry
from common.service_base import ServiceBase
from .api.node_management import ApiNodeManagement
from .api.schedule import ApiSchedule
from .api.task import ApiTask
from .configuration_manager import ConfigurationManager
from .db_caching.queue_cache import QueueCache
from .db_interface import DbInterface
from .scrape_node_list import ScrapeNodeList
from .message_queue_thread import MessageQueueThread

class Service(ServiceBase):
    #pylint: disable=too-many-instance-attributes
    """ Siterummage Big Broker microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Big Broker Microservice'

    def __init__(self, new_instance):
        super().__init__()

        self._quart = new_instance

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceThread
        self._is_initialised = False

        self._configuration = None
        self._messaging_config = None
        self._api_schedule = None
        self._api_node_management = None
        self._api_task = None
        self._scrape_node_list = ScrapeNodeList()
        self._crypto_utils = CryptoUtils()
        self._messaging_thread = None
        self._queue_cache = None
        self._db_interface = None

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info, f'{self.title_text} {CORE_VERSION}' + \
                         f'-{BUILD_NO}')
        self._logger.log(LogType.Info, COPYRIGHT_TEXT)
        self._logger.log(LogType.Info, LICENSE_TEXT)

        config_mgr = ConfigurationManager()
        config_file = os.getenv('SITERUMMAGE_BIGBROKER_CONFIG')
        self._logger.log(LogType.Info, f'Master config file: {config_file}')
        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        messaging_config_mgr = MessagingQueueConfigManager()
        queue_config_file = os.getenv('SITERUMMAGE_BIGBROKER_MESSAGING_CONFIG')
        self._logger.log(LogType.Info,
                         f'Messaging config file: {queue_config_file}')
        self._messaging_config = messaging_config_mgr.parse(queue_config_file)
        if not self._messaging_config:
            self._logger.log(LogType.Error,
                             messaging_config_mgr.last_error_msg)
            return False

        self._display_configuration_settings()

        self._api_schedule = ApiSchedule(self._quart, self._configuration)

        big_broker_cfg = self._configuration.big_broker_api

        status, err =  self._crypto_utils.load_private_key(big_broker_cfg.private_key)
        if not status:
            self._logger.log(LogType.Critical, err)
            return False

        self._logger.log(LogType.Info, 'Private PKI key loaded...')

        status, err =  self._crypto_utils.load_public_key(big_broker_cfg.public_key)
        if not status:
            self._logger.log(LogType.Critical, err)
            return False

        self._logger.log(LogType.Info, 'Public PKI key loaded...')

        if not self._open_url_processing_db():
            return False

        self._queue_cache = QueueCache(self._db_interface, self._configuration,
                                       self._logger)

        self._api_node_management = ApiNodeManagement(self._quart,
                                                      self._configuration,
                                                      self._scrape_node_list,
                                                      self._logger,
                                                      self._crypto_utils)

        self._api_task = ApiTask(self._quart, self._configuration,
                                 self._logger)

        self._create_message_queue_thread()

        self._is_initialised = True

        return True

    def _open_url_processing_db(self):
        db_settings_cfg = self._configuration.db_settings

        self._db_interface = DbInterface(db_settings_cfg.database_file)

        if not self._db_interface.database_exists():
            if self._configuration.db_settings.fail_on_no_database:
                self._logger.log(LogType.Error,
                                 "DB doesn't exist and fail on create is set")
                return False

            if not self._db_interface.build_database():
                self._logger.log(LogType.Error,
                                 self._db_interface.last_error_message)
                return False

            self._logger.log(LogType.Info, 'Database created successfully')

        else:
            self._logger.log(LogType.Info, 'Database already exists')

        if not self._db_interface.open():
            self._logger.log(LogType.Error,
                             self._db_interface.last_error_message)
            return False

        return True

    def _display_configuration_settings(self):
        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        page_store_cfg = self._configuration.page_store_api
        self._logger.log(LogType.Info, 'Page Store Api :->')
        self._logger.log(LogType.Info, f'+= host : {page_store_cfg.host}')
        self._logger.log(LogType.Info, f'+= port : {page_store_cfg.port}')
        self._logger.log(LogType.Info, '+==============================+')
        big_broker_cfg = self._configuration.big_broker_api
        self._logger.log(LogType.Info, 'Big Broker Api :->')
        self._logger.log(LogType.Info,
                         f'+= Private Key file : {big_broker_cfg.private_key}')
        self._logger.log(LogType.Info,
                         f'+= Public Key File  : {big_broker_cfg.public_key}')
        self._logger.log(LogType.Info, '+==============================+')
        db_settings_cfg = self._configuration.db_settings
        self._logger.log(LogType.Info, 'Database Settings :->')
        self._logger.log(LogType.Info,
                         f'+= Cache size : {db_settings_cfg.cache_size}')
        self._logger.log(LogType.Info,
                         f'+= database file : {db_settings_cfg.database_file}')
        self._logger.log(LogType.Info,
                         f'+= Fail on no db : {db_settings_cfg.fail_on_no_database}')
        self._logger.log(LogType.Info, '+==============================+')
        cfg = self._messaging_config.connection_settings
        self._logger.log(LogType.Info, 'Messaging Service Settings :->')
        self._logger.log(LogType.Info, '  Connection Settings')
        self._logger.log(LogType.Info, f'+= Service host : {cfg.host}')
        self._logger.log(LogType.Info, f'+= Username : {cfg.username}')
        self._logger.log(LogType.Info, '+= Password : <REDACTED>')

        cfg = self._messaging_config.consumer_settings
        if cfg:
            self._logger.log(LogType.Info, '  Consumer queue')
            self._logger.log(LogType.Info, '+= Queue name : ' + \
                f'{cfg.queue.name}')
            self._logger.log(LogType.Info, '+= Is durable : ' + \
                f'{cfg.queue.is_durable}')

        cfg = self._messaging_config.producers_settings
        if cfg:
            for queue in cfg.queues:
                self._logger.log(LogType.Info, '  Producer queue :->')
                self._logger.log(LogType.Info, '+= Queue  name : ' + \
                    f'{queue.name}')
                self._logger.log(LogType.Info, '+= Is durable : ' + \
                    f'{queue.is_durable}')

        self._logger.log(LogType.Info, '+==============================+')

    def _create_message_queue_thread(self) -> None:
        conn_settings = self._messaging_config.connection_settings
        consumer_settings = self._messaging_config.consumer_settings

        settings = MessagingQueueSettings()
        settings.connection_settings.username = conn_settings.username
        settings.connection_settings.password = conn_settings.password
        settings.connection_settings.host = conn_settings.host

        settings.queue_consumer_definition.queue.is_durable = \
            consumer_settings.queue.is_durable
        settings.queue_consumer_definition.queue.name = \
            consumer_settings.queue.name
        settings.queue_consumer_definition.queue.exchange_binding = \
            consumer_settings.queue.exchange_binding
        settings.queue_consumer_definition.queue.exchange_routing_keys = \
            consumer_settings.queue.exchange_routing_keys

        if self._messaging_config.producers_settings:
            for producer in self._messaging_config.producers_settings.queues:
                entry = QueueEntry()
                entry.name = producer.name
                entry.is_durable = producer.is_durable
                settings.publishing_queues.add_queue(entry)

        if self._messaging_config.exchanges_settings:
            for exchange in self._messaging_config.exchanges_settings.exchanges:
                entry = ExchangeEntry()
                entry.name = exchange.name
                entry.exchange_type = exchange.exchange_type
                settings.exchanges.add(entry)

        self._messaging_thread = MessageQueueThread(settings, self._logger)
        self._messaging_thread.start()

    async def _main_loop(self) -> None:
        cached_entries = self._get_cached_queue_entries()

        if cached_entries:
            self._add_cached_entries_to_message_queue(cached_entries)

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
        self._messaging_thread.stop()
        self._messaging_thread.join()

        if self._db_interface.is_connected:
            self._db_interface.close()
            self._logger.log(LogType.Info, '|-> Database connection closed')

    def _get_cached_queue_entries(self) -> list:
        """!@brief Get a list of cached queue from queue database, the number
                   of entries depends on the size/length of the current cache
                   queue and the configurable size of queue from the config.
        @param self The object pointer.
        @returns Variable lengthed list of queue entries, enpty if none are
                 required or available.
        """

        queue_size = self._queue_cache.size_all_queue

        if queue_size < self._configuration.db_settings.cache_size:
            get_size = queue_size - self._configuration.db_settings.cache_size

            return self._db_interface.get_queue_cache(get_size)

        return []

    def _add_cached_entries_to_message_queue(self, entries):

        routing_key = 'urls_to_be_processed'

        self._logger.log(LogType.Info,
                         f'Cached {len(entries)} new db entries...')
        id_list = list(map(itemgetter('id'), entries))
        self._db_interface.set_ids_to_cached(id_list)

        for entry in entries:
            task_type = 'New' if entry['link_type'] == 0 else 'Rescan'
            message_body = {
                'url': entry['url'],
                'task_type': task_type,
                'task_id': entry['task_id']
            }
            self._messaging_thread.queue_consumer.publish_message(
                '', routing_key, json.dumps(message_body))
