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
import os
import time
from typing import Tuple
import uuid
import requests
import jsonschema
import common.api_contracts.big_broker.node_management as schemas
from common.crypto_utils import CryptoUtils
from common.event import Event
from common.event_manager import EventManager
from common.http_status_code import HTTPStatusCode
from common.logger import Logger, LogType
from common.message_queue_config_mananger import MessagingQueueConfigManager
from common.messaging_queue_settings import MessagingQueueSettings, QueueEntry
from common.mime_type import MIMEType
from common.info import BUILD_NO, COPYRIGHT_TEXT, CORE_VERSION, LICENSE_TEXT
from configuration_manager import ConfigurationManager
from event_id import EventID
from page_scraper import PageScraper
from scrape_node.worker_thread import WorkerThread

class ScrapeNodeApp:
    ''' Entrypoint wrapper class for the scrape node application '''
    __slots__ = ['_configuration', '_crypto_utils', '_event_manager',
                 '_is_initialised', '_logger', '_messaging_config',
                 '_page_scraper', '_public_key',
                 '_worker_thread', '_worker_thread_run_flag']

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Scrape Node'

    @property
    def is_initialised(self) -> bool:
        """!@brief is_initialised property (getter).
        @param self The object pointer.
        @return True if is_initialised, else False.
        """
        return self._is_initialised

    def __init__(self):
        """!@brief Default constructor.
        @param self The object pointer.
        """

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceBase
        self._is_initialised = False

        self._public_key = ''
        self._event_manager = EventManager()
        self._page_scraper = PageScraper(self._logger, self._event_manager)
        self._configuration = None
        self._messaging_config = None
        self._crypto_utils = None
        self._worker_thread = None

    def start(self) -> None:
        """!@brief ** Overridable 'run' function **
        Start the application.
        @param self The object pointer.
        @return None
        """

        if not self._is_initialised:
            raise RuntimeError('Not initialised')

        try:
            while True:
                self._main_loop()
                time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        # Perform any shutdown required.
        self._shutdown()

    def initialise(self) -> bool:
        """!@brief Service initialisation function
        Successful initialisation should set self._initialised to True.
        @param self The object pointer.
        @return True if initialise was successful, otherwise False.
        """
        self._logger.write_to_console = True
        self._logger.initialise()

        self._logger.log(LogType.Info, f'{self.title_text} {CORE_VERSION}' + \
                         f'-{BUILD_NO}')
        self._logger.log(LogType.Info, COPYRIGHT_TEXT)
        self._logger.log(LogType.Info, LICENSE_TEXT)

        config_mgr = ConfigurationManager()

        config_file = os.getenv('SITERUMMAGE_SCRAPENODE_CONFIG')

        self._configuration = config_mgr.parse_config_file(config_file)
        if not self._configuration:
            self._logger.log(LogType.Error, config_mgr.last_error_msg)
            return False

        messaging_config_mgr = MessagingQueueConfigManager()
        queue_config_file = os.getenv('SITERUMMAGE_SCRAPENODE_MESSAGING_CONFIG')
        self._logger.log(LogType.Info,
                         f'Messaging config file: {queue_config_file}')
        self._messaging_config = messaging_config_mgr.parse(queue_config_file)
        if not self._messaging_config:
            self._logger.log(LogType.Error,
                             messaging_config_mgr.last_error_msg)
            return False

        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        cfg = self._configuration.big_broker_api
        self._logger.log(LogType.Info, '+== Big Broker Api Settings :->')
        self._logger.log(LogType.Info, f'+= API Endpoint : {cfg.api_endpoint}')
        self._logger.log(LogType.Info, '+= Auth Key : REDACTED')
        cfg = self._configuration.page_store_api
        self._logger.log(LogType.Info, '+== Page Store Api Settings :->')
        self._logger.log(LogType.Info, f'+= API Host : {cfg.api_endpoint}')
        self._logger.log(LogType.Info, '+= Page Store Auth Key : ***')
        conf = self._configuration.api_settings
        self._logger.log(LogType.Info, '+== Api Settings :->')
        self._logger.log(LogType.Info,
                         f'+= Private Key File : {conf.private_key_file}')
        self._logger.log(LogType.Info,
                         f'+= Public Key File  : {conf.public_key_file}')
        self._logger.log(LogType.Info,
                          '+= Auth Key         : ***')
        self._logger.log(LogType.Info, '+==============================+')

        self._crypto_utils = CryptoUtils()

        public_key = self._configuration.api_settings.public_key_file
        status, err = self._crypto_utils.load_public_key(public_key)
        if not status:
            self._logger.log(LogType.Critical, err)
            return False

        self._logger.log(LogType.Info, 'Public PKI key loaded...')

        private_key = self._configuration.api_settings.private_key_file
        status, err = self._crypto_utils.load_private_key(private_key)
        if not status:
            self._logger.log(LogType.Critical, err)
            return False

        self._logger.log(LogType.Info, 'Private PKI key loaded...')

        try:
            status, err_msg = self._register_with_big_broken()
            if not status:
                self._logger.log(LogType.Critical,
                                'Unable to register node with big broker, ' + \
                                    f'reason: {err_msg}')
                return False

        except KeyboardInterrupt:
            self._shutdown()
            return False

        self._register_event_handlers()

        self._create_message_queue_thread()

        self._is_initialised = True

        return True

    def shutdown(self) -> None:
        """!@brief Wrap the overridable 'shutdown' function
        @param self The object pointer.
        @return None
        """
        return self._shutdown()

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

        self._worker_thread = WorkerThread(settings, self._logger,
                                           self._page_scraper)
        self._worker_thread.start()

    def _main_loop(self) -> None:
        """!@brief Overridable 'main loop' function **
        @param self The object pointer.
        @return None
        """
        self._event_manager.process_next_event_sync()


    def _shutdown(self) -> None:
        """!@brief Overridable 'shutdown' function **
        @param self The object pointer.
        @return None
        """
        self._logger.log(LogType.Info, 'Shutting down...')

        if self._worker_thread:
            self._logger.log(LogType.Info, '=> Stopping messaging service...')
            self._worker_thread.stop()
            self._worker_thread.join()

        self._logger.log(LogType.Info, 'Shutdown cleanup complete...')

    def _register_with_big_broken(self) -> Tuple[bool, str]:
        """!@brief Register the scraper node instance with Big Broker, this is
                   done by generating an identifier using the hostanme and port
                   it is using and then encrypted using Big Brokers public key.
        @param self The object pointer.
        @returns Tuple of [bool, str], if bool is true then registration was
                 successful, the string value should be empty. Upon a failure
                 the bool is false and the string is populated with an error.
        """

        headers = {
            'AuthKey': self._configuration.big_broker_api.auth_key,
            'Content-type': MIMEType.JSON
        }

        ident_raw = str(uuid.uuid1())
        identifier = self._crypto_utils.encrypt(ident_raw, encode_base64=True)

        body = { "identifier": identifier }

        response = None

        url = f'{self._configuration.big_broker_api.api_endpoint}' + \
            '/nodemanager/add'

        while response is None:

            try:
                response = requests.post(url, data=json.dumps(body),
                                         headers=headers)

            except requests.exceptions.RequestException:
                time.sleep(1)
                err = 'Failed to register with big broker, retying...'
                self._logger.log(LogType.Critical, err)

        status_code = response.status_code

        if status_code != HTTPStatusCode.OK:
            return False, 'Bad node registration response status ' + \
                f'({status_code}, error: {response.text}'

        body = response.json()

        try:
            jsonschema.validate(body, schemas.NodeManagerAddResponse.schema)

        except jsonschema.exceptions.ValidationError:
            return False, 'Unable to validate node registration response.'

        username, err = self._crypto_utils.decrypt(
            body[schemas.NodeManagerAddResponse.queue_username], True)
        if not username:
            return False, f'Cannot decrypt username, reason: {err}'

        password, err = self._crypto_utils.decrypt(
            body[schemas.NodeManagerAddResponse.queue_password], True)
        if not password:
            return False, f'Cannot decrypt password, reason: {err}'

        return True, ''

    def _register_event_handlers(self) -> None:
        """!@brief Register event and callback events.
        @param self The object pointer.
        @returns None.
        """

        # =====================
        # == Register events ==
        # ======================

        # Event: Store results.
        self._event_manager.register_event(EventID.StoreResults,
                                           self._store_results)

        # Event: Add links to queue.
        self._event_manager.register_event(EventID.AddLinksToQueue,
                                           self._add_links_to_queue)

        # Event: Add links to queue.
        self._event_manager.register_event(EventID.SendCompleteTask,
                                           self._send_complete_task)

        # ==============================
        # == Register callback events ==
        # ==============================

        # Register Callback event: Get url being processed.
        self._event_manager.register_callback_event(
            EventID.GetUrlBeingProcessed, self._handle_get_url_being_processed)

    def _handle_get_url_being_processed(self, event):
        #pylint: disable=unused-argument
        return self._page_scraper.url_being_processed

    def _store_results(self, event):

        details = event.body['details']

        task_id = event.body['task_id']

        self._logger.log(LogType.Info, "Posting results to Page Store...")

        message_body = {
            "general_settings":
            {
                "domain": details.domain,
                "url_path": details.url_path,
                "hash": details.page_hash,
                "successfully_read": event.body['success']
            },
            "metadata":
            {
                "title": details.title,
                "abstract": details.description,
            }
        }

        settings = self._configuration.page_store_api
        endpoint = f'{settings.api_endpoint}/webpage/add'

        headers = {
            'AuthKey': self._configuration.page_store_api.auth_key,
            'Content-type': MIMEType.JSON
        }

        try:
            response = requests.post(endpoint, headers=headers,
                                     data=json.dumps(message_body))

        except requests.exceptions.RequestException:
            err = 'Post results to Page Store failed, a retry will occur ' + \
                ' in 10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)
            return

        status_code = response.status_code

        # If OK or NotAcceptable (page url already exists) then just continue.
        if status_code in [HTTPStatusCode.OK, HTTPStatusCode.NotAcceptable]:

            if not event.body['success']:
                return

            add_links_event_body = {
                'links': event.body['links'],
                'task_id' : task_id
            }
            send_link_event = Event(EventID.AddLinksToQueue, add_links_event_body)
            self._event_manager.queue_event(send_link_event)

        else:
            err = 'Post results to Page Store failed, status code ' + \
                f'{status_code} ({response.text}), a retry will occur in 10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)

    def _add_links_to_queue(self, event):

        self._logger.log(LogType.Info, 'Sending links to broker')

        settings = self._configuration.processing_queue_api
        endpoint = f'{settings.api_endpoint}/queue/add'

        headers = {
            'AuthKey': settings.auth_key,
            'Content-type': MIMEType.JSON
        }

        links = []
        for link in event.body['links']:
            entry = {
                "url": link
            }

            links.append(entry)

        message_body = {
            'links': links
        }

        try:
            response = requests.post(endpoint, headers=headers,
                                     data=json.dumps(message_body))

        except requests.exceptions.RequestException:
            err = 'Adding links to Processing Queue failed, a retry will ' + \
                'occur in 10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)
            return

        status_code = response.status_code

        # If OK or NotAcceptable (page url already exists) then just continue.
        if status_code == HTTPStatusCode.OK:

            self._logger.log(LogType.Info,
                             'Links successfully added to the processing queue')

            event_body = {
                'task_id': event.body['task_id']
            }
            send_complete_event = Event(EventID.SendCompleteTask, event_body)
            self._event_manager.queue_event(send_complete_event)

        else:
            err = 'Post results to Processing Queue failed, status code ' + \
                f'{status_code} ({response.text}), a retry will occur in ' + \
                 '10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)

    def _send_complete_task(self, event):

        self._logger.log(LogType.Info,
                            'Sending task completion message to Big Broker...')

        event_body = event.body

        settings = self._configuration.big_broker_api
        endpoint = f'{settings.api_endpoint}/task/complete_task'

        headers = {
            'AuthKey': settings.auth_key,
            'Content-type': MIMEType.JSON
        }

        message_body = {
            "task_id": event_body['task_id'],
            "is_successful": self._page_scraper.was_scrape_successful
        }

        try:
            response = requests.post(endpoint, headers=headers,
                                     data=json.dumps(message_body))

        except requests.exceptions.RequestException:
            err = 'Sending task completion failed, a retry will occur ' + \
                'in 10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)
            return

        status_code = response.status_code

        # If OK or NotAcceptable (page url already exists) then just continue.
        if status_code == HTTPStatusCode.OK:

            self._logger.log(LogType.Info,
                             'Successfully Sent task complete to Big Broker')

        else:
            err = 'Sending task completion failed, status code ' + \
                f'{status_code} ({response.text}), a retry will occur in ' + \
                 '10 seconds...'
            self._logger.log(LogType.Critical, err)
            event.trigger_time = 10000
            self._event_manager.queue_event(event)
