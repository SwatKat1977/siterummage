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
import os
from common.logger import Logger, LogType
from common.info import BUILD_NO, COPYRIGHT_TEXT, CORE_VERSION, LICENSE_TEXT
from common.message_queue_config_mananger import MessagingQueueConfigManager
from common.messaging_queue_settings import MessagingQueueSettings, QueueEntry
from common.service_base import ServiceBase
from .api.health import ApiHealth
from .api.webpage import ApiWebpage
from .configuration_manager import ConfigurationManager
from .database_interface import DatabaseInterface
from .message_queue_thread import MessageQueueThread

class Service(ServiceBase):
    """ Siterummage Page Store microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Page Store Microservice'

    def __init__(self, new_instance):
        super().__init__()

        self._quart = new_instance

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceThread
        self._is_initialised = False

        self._configuration = None

        self._db_interface = None

        self._api_health = ApiHealth(self._quart)
        self._api_webpage = None
        self._messaging_config = None

    def _initialise(self) -> bool:
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info, f'{self.title_text} {CORE_VERSION}' + \
                         f'-{BUILD_NO}')
        self._logger.log(LogType.Info, COPYRIGHT_TEXT)
        self._logger.log(LogType.Info, LICENSE_TEXT)

        config_mgr = ConfigurationManager()

        config_file = os.getenv('SITERUMMAGE_PAGESTORE_CONFIG')

        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        messaging_config_mgr = MessagingQueueConfigManager()
        queue_config_file = os.getenv('SITERUMMAGE_PAGESTORE_MESSAGING_CONFIG')
        self._logger.log(LogType.Info,
                         f'Messaging config file: {queue_config_file}')
        self._messaging_config = messaging_config_mgr.parse(queue_config_file)
        if not self._messaging_config:
            self._logger.log(LogType.Error,
                             messaging_config_mgr.last_error_msg)
            return False

        self._display_configuration_settings()

        self._db_interface = DatabaseInterface(self._logger,
                                               self._configuration)

        if not self._db_interface.database_connection_valid():
            return False

        self._create_message_queue_thread()

        self._api_webpage = ApiWebpage(self._quart, self._db_interface,
                                       self._configuration)

        self._is_initialised = True

        return True

    def _display_configuration_settings(self):
        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        db_config = self._configuration.db_settings
        self._logger.log(LogType.Info, '+== Database Settings :->')
        self._logger.log(LogType.Info, f'+= database  : {db_config.database}')
        self._logger.log(LogType.Info, f'+= host      : {db_config.host}')
        self._logger.log(LogType.Info, f'+= username  : {db_config.username}')
        self._logger.log(LogType.Info, f'+= port      : {db_config.port}')
        self._logger.log(LogType.Info, f'+= pool_name : {db_config.pool_name}')
        self._logger.log(LogType.Info, f'+= pool_size : {db_config.pool_size}')
        self._logger.log(LogType.Info, '+==============================+')

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
        producers_settings = self._messaging_config.producers_settings

        settings = MessagingQueueSettings()
        settings.connection_settings.username = conn_settings.username
        settings.connection_settings.password = conn_settings.password
        settings.connection_settings.host = conn_settings.host
        settings.queue_consumer_definition.queue.is_durable = \
            consumer_settings.queue.is_durable
        settings.queue_consumer_definition.queue.name = \
            consumer_settings.queue.name

        for producer in producers_settings.queues:
            entry = QueueEntry()
            entry.name = producer.name
            entry.is_durable = producer.is_durable
            settings.publishing_queues.add_queue(entry)

        self._messaging_thread = MessageQueueThread(settings, self._logger)
        self._messaging_thread.start()

    async def _main_loop(self):
        # if not self._master_thread_class.initialise():
        #     return False
        pass

    def _shutdown(self):
        self._logger.log(LogType.Info, 'Shutting down...')
        self._messaging_thread.stop()
        self._messaging_thread.join()
