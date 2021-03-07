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
import time
from threading import Thread
from common.logger import Logger, LogType
from common.messaging_queue import MessagingQueue
from common.messaging_queue_settings import MessagingQueueSettings
from page_scraper import PageScraper

class WorkerThread(Thread):
    """ Thread to handle RabbitMQ Messaging Queue """

    processed_results_queue = 'processing_results_queue'

    @property
    def queue_consumer(self) -> MessagingQueue:
        """!@brief Queue consumer object instance (Getter).
        @param self The object pointer.
        @returns MessagingQueue.
        """
        return self._queue_consumer

    def __init__(self, settings : MessagingQueueSettings,
                 logger : Logger, scraper : PageScraper) -> None:
        super().__init__()

        self._logger = logger
        self._queue_consumer = MessagingQueue(settings, logger)
        self._queue_consumer.set_message_processor(self._receive_new_task)
        self._thread_running = False
        self._page_scraper = scraper
        self._reconnect_delay = 0
        self._settings = settings

    def run(self) -> None:
        """!@brief Overridable method called when the thread runs, it will keep
                   running until _thread_running is set to false.  If there is
                   a disconnect then it will attempt reconnect.
        @param self The object pointer.
        @returns None.
        """

        self._logger.log(LogType.Info, 'Running messaging queue in a thread')
        self._thread_running = True

        while self._thread_running:
            self._queue_consumer.start()
            self._maybe_reconnect()

    def stop(self) -> None:
        """!@brief Method called to stop the thread runs, it will perform a
                   a shutdown on the consumer closing the connection and doing
                   a tidy up.
        @param self The object pointer.
        @returns None.
        """

        self._thread_running = False
        self._queue_consumer.shutdown()

    def _maybe_reconnect(self):

        if self._queue_consumer.should_reconnect:
            self._queue_consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            self._logger.log(LogType.Info,
                f'Reconnecting after {reconnect_delay} seconds')
            time.sleep(reconnect_delay)
            self._queue_consumer.reset_for_reconnect()

    def _receive_new_task(self, _channel, method, _properties, body):
        msg_body = json.loads(body)
        url = msg_body['url']
        task_type = msg_body['task_type']
        task_id = msg_body['task_id']

        self._logger.log(LogType.Info,
                         f'Initiated new scrape task for url {url}')
        links, results = self._page_scraper.scrape_page(url, task_type, task_id)
        if links:
            body = { 'link': links }
            print(body)
            self._queue_consumer.publish_message('', 
                                                 self.processed_results_queue,
                                                 json.dumps(body))

        self._queue_consumer.publish_message('', 
                                             self.processed_results_queue,
                                             json.dumps(results))

        self._queue_consumer.acknowledge_message(method.delivery_tag)

    def _get_reconnect_delay(self):
        if self._queue_consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 2
        if self._reconnect_delay > 60:
            self._reconnect_delay = 60
        return self._reconnect_delay
