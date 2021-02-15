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
import base64
import json
import os
import socket
import time
from typing import Tuple
import uuid
import requests
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from common.event import Event
from common.event_manager import EventManager
from common.http_status_code import HTTPStatusCode
from common.logger import Logger, LogType
from common.mime_type import MIMEType
from common.info import BUILD_NO, COPYRIGHT_TEXT, CORE_VERSION, LICENSE_TEXT
from common.service_base import ServiceBase
from .api.job import ApiJob
from .configuration_manager import ConfigurationManager
from .event_id import EventID
from .page_scraper import PageScraper

class Service(ServiceBase):
    """ Siterummage Scrape Node microservice class """

    ## Title text logged during initialisation.
    title_text = 'Site Rummagge Scrape Node'

    def __init__(self, quart_instance):
        """!@brief Scrape Node service class constructor.
        @param self The object pointer.
        @param quart_instance Instance of the Quart application.
        @returns Service instance.
        """
        super().__init__()

        self._quart = quart_instance

        ## Instance of the logging wrapper class
        self._logger = Logger()

        ## _is_initialised is inherited from parent class ServiceBase
        self._is_initialised = False

        self._public_key = ''

        self._server_id = str(uuid.uuid4())

        self._api_job = None

        self._event_manager = EventManager()

        self._page_scraper = PageScraper(self._logger, self._event_manager)

        self._configuration = None

    def _initialise(self) -> bool:
        """!@brief Override for the initialise service method.
        @param self The object pointer.
        @returns Boolean to show if initialisation was successful or not.
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

        self._logger.log(LogType.Info, '+=== Configuration Settings ===+')
        self._logger.log(LogType.Info, '+==============================+')
        cfg = self._configuration.big_broker_api
        self._logger.log(LogType.Info, '+== Big Broker Api Settings :->')
        self._logger.log(LogType.Info, f'+= API Endpoint : {cfg.api_endpoint}')
        self._logger.log(LogType.Info, '+= Auth Key : REDACTED')
        cfg = self._configuration.page_store_api
        self._logger.log(LogType.Info, '+== Page Store Api Settings :->')
        self._logger.log(LogType.Info, f'+= API Host : {cfg.api_endpoint}')
        self._logger.log(LogType.Info, '+= Auth Key : REDACTED')
        conf = self._configuration.api_settings
        self._logger.log(LogType.Info, '+== Api Settings :->')
        self._logger.log(LogType.Info,
                         f'+= Public Key File : {conf.public_key_file}')
        self._logger.log(LogType.Info,
                          '+= Auth Key        : REDACTED')
        cfg = self._configuration.processing_queue_api
        self._logger.log(LogType.Info, '+== Processing Queue Api Settings :->')
        self._logger.log(LogType.Info, f'+= API Host : {cfg.api_endpoint}')
        self._logger.log(LogType.Info, '+= Auth Key : REDACTED')
        self._logger.log(LogType.Info, '+==============================+')

        self._api_job = ApiJob(self._quart, self._logger, self._event_manager)

        if not self._load_public_key():
            return False

        status, err_msg = self._register_with_big_broken()
        if not status:
            self._logger.log(LogType.Critical,
                             'Unable to register node with big broker, ' + \
                                 f'reason: {err_msg}')
            return False

        self._register_event_handlers()

        self._is_initialised = True

        return True

    async def _main_loop(self) -> None:
        """!@brief Override for the main service method.
        @param self The object pointer.
        @returns None.
        """

        await self._event_manager.process_next_event()

    def _shutdown(self) -> None:
        """!@brief Override for the shutdown service method.
        @param self The object pointer.
        @returns None.
        """
        self._logger.log(LogType.Info, 'Shutting down...')

    def _load_public_key(self) -> bool:
        """!@brief Attempt to load the public key used by Site Rummage.
        @param self The object pointer.
        @returns Boolean : True = success, False = failed.
        """

        key_filename = self._configuration.api_settings.public_key_file

        self._logger.log(LogType.Info, f"Loading public key '{key_filename}'")

        try:
            with open(key_filename, 'r') as file_handle:
                file_contents = file_handle.read()

        except FileNotFoundError as io_except:
            err = f"Unable to read public key '{key_filename}', reason: " + \
                str(io_except)
            self._logger.log(LogType.Critical, err)
            return False

        self._public_key = RSA.import_key(file_contents)

        self._logger.log(LogType.Info, "Public key Loaded...")

        return True

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

        network_port = os.getenv('SITERUMMAGE_SCRAPENODE_PORT')
        host = socket.gethostname()

        ident_raw = str.encode(f"NODE_{host}_{network_port}")
        cipher = PKCS1_OAEP.new(key=self._public_key)
        identifier = cipher.encrypt(ident_raw)
        identifier = base64.b64encode(identifier)
        identifier = identifier.decode('ascii')

        body = {
            "identifier": identifier,
            "host": socket.gethostname(),
            "port": int(os.getenv('SITERUMMAGE_SCRAPENODE_PORT'))
        }

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

        if status_code == HTTPStatusCode.OK:
            return True, ''

        if status_code == HTTPStatusCode.NotFound:
            return False, 'Bad API endpoint specified'

        if status_code == HTTPStatusCode.BadRequest:
            return False, f'Bad request - {response.text}'

        if status_code in [HTTPStatusCode.Unauthenticated,
                           HTTPStatusCode.Forbidden]:
            return False, 'API token invalid or missing!'

        return False, f'Status code {status_code}'

    def _register_event_handlers(self) -> None:
        """!@brief Register event and callback events.
        @param self The object pointer.
        @returns None.
        """

        # =====================
        # == Register events ==
        # ======================

        # Event: New scrape task.
        self._event_manager.register_event(EventID.NewScrapeTask,
                                           self._initiate_new_scrape_task)

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

    def _initiate_new_scrape_task(self, event):
        body = event.body
        url = body['url']
        task_type = body['task_type']
        task_id = body['task_id']

        self._logger.log(LogType.Info,
                         f'Initiated new scrape task for url {url}')
        self._page_scraper.scrape_page(url, task_type, task_id)

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
