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
from dataclasses import dataclass
import functools
from typing import Any
import pika
from common.logger import Logger, LogType
from common.messaging_queue_settings import MessagingQueueSettings

@dataclass
class MessagingQueueState:
    fatal_close: bool = False
    is_connected: bool = False
    is_consuming: bool = False
    perform_close: bool = False
    should_reconnect: bool = False
    shutdown_complete: bool = False
    was_consuming: bool = False

class MessagingQueue:
    ''' Wrapper class for RabbitMQ functionality '''
    __slots__ = ['_channel', '_connection', '_consumer_tag',
                  '_logger', '_message_processor', '_parameters',
                  '_queue_state', '_settings']

    RABBIT_PRECONDITION_FAILED = 406

    @property
    def was_consuming(self) -> bool:
        """!@brief Was queue consuming flag (getter).
        @param self The object pointer.
        @returns bool identifying state.
        """
        return self._queue_state.was_consuming

    @property
    def should_reconnect(self) -> bool:
        """!@brief Should reconnect flag (getter).
        @param self The object pointer.
        @returns bool identifying state.
        """
        return self._queue_state.should_reconnect and not self._queue_state.fatal_close

    def __init__(self, settings : MessagingQueueSettings,
                 logger : Logger) -> Any:

        self._logger = logger
        self._settings = settings

        self._channel = None
        self._connection = None
        self._consumer_tag = None
        self._queue_state = MessagingQueueState()
        self._message_processor = None

        credentials = pika.PlainCredentials(
            self._settings.connection_settings.username,
            self._settings.connection_settings.password)
        self._parameters = pika.ConnectionParameters(
            self._settings.connection_settings.host, credentials=credentials)

    def set_message_processor(self, processor):
        """!@brief Set the message processor method.
        @param self The object pointer.
        @param processor Message processor method.
        @returns None.
        """
        self._message_processor = processor

    def start(self) -> None:
        """!@brief Start the messaging queue, which runs forever until the
                   application closes or a reconnect needs to occur.
        @param self The object pointer.
        @returns None.
        """

        self._logger.log(LogType.Info, 'Messaging | Starting...')
        self._connect()
        self._connection.ioloop.start()
        self._logger.log(LogType.Info, 'Messaging | Ended...')

    def stop(self) -> None:
        """!@brief Stop the messaging queue, ensuring the ioloop is stopped and
                   the consumer, possibly for reconnect.
        @param self The object pointer.
        @returns None.
        """

        if not self._queue_state.perform_close:
            self._queue_state.perform_close = True

            self._logger.log(LogType.Info, 'Messaging | Stopping...')

            if self._queue_state.is_consuming:
                self._stop_consuming()
            else:
                self._connection.ioloop.stop()

    def shutdown(self):
        self._logger.log(LogType.Info, 'Messaging | Shutting down...')

        if self._queue_state.is_consuming:
            self._stop_consuming()

        if self._connection:
            self._connection.ioloop.stop()

    def acknowledge_message(self, delivery_tag) -> None:
        """!@brief Publish a message to the queue.
        @param self The object pointer.
        @param delivery_tag Delivery tag to identify what to acknowledge.
        @returns None.
        """
        self._channel.basic_ack(delivery_tag)

    def publish_message(self, exchange, routing_key, body) -> None:
        """!@brief Publish a message to the queue.
        @param self The object pointer.
        @param exchange Exchange to publish to.
        @param routing_key Routing key for published message.
        @param body Body of message.
        @returns None.
        """

        if not self._queue_state.is_connected:
            raise RuntimeError('Not connected to message queue')

        self._channel.basic_publish(exchange=exchange,
                                    routing_key=routing_key, body=body)

    def reset_for_reconnect(self) -> None:
        """!@brief Reset the messaging queue ready for reconnect attempt.
        @param self The object pointer.
        @returns None.
        """
        self._channel = None
        self._connection = None
        self._consumer_tag = None
        self._queue_state.is_connected = False
        self._queue_state.is_consuming = False
        self._queue_state.perform_close = False
        self._queue_state.should_reconnect = False
        self._queue_state.shutdown_complete = False
        self._queue_state.was_consuming = False

    def _connect(self):
        self._connection = pika.SelectConnection(
            parameters=self._parameters, on_open_callback=self._on_connection_open,
            on_open_error_callback=self._on_connection_open_error,
            on_close_callback=self._on_connection_closed)

    def _on_connection_open(self, _unused_connection):
        self._logger.log(LogType.Info, 'Messaging | Connection opened')
        self._queue_state.is_connected = True
        self._connection.channel(on_open_callback=self._on_channel_open)

    def _on_channel_open(self, channel):
        self._logger.log(LogType.Info, 'Messaging | New channel created')

        self._channel = channel
        self._logger.log(LogType.Info, 'Messaging | Adding channel close callback')
        self._channel.add_on_close_callback(self._on_channel_closed)

        queue_name = self._settings.queue_consumer_definition.queue.name
        is_durable = self._settings.queue_consumer_definition.queue.is_durable

        # Declare queue for processed urls results and bind it to exchange.
        self._logger.log(LogType.Info,
                         f"Messaging | Creating queue '{queue_name}'")
        callback = functools.partial(self._on_queue_declare_ok,
                                     userdata=queue_name)
        self._channel.queue_declare(
            queue=queue_name, durable=is_durable, callback=callback)

    def _on_channel_closed(self, _channel, reason):

        if reason.reply_code == self.RABBIT_PRECONDITION_FAILED:
            self._logger.log(LogType.Critical,
                f"Channel was closed due to {reason.reply_text}")
            self._queue_state.fatal_close = True

        else:
            self._logger.log(LogType.Info, "Messaging | Channel was closed")

        self._queue_state.is_consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            self._logger.log(LogType.Info,
                             'Connection is closing or already closed')

        else:
            self._logger.log(LogType.Info, 'Closing the connection')
            self._connection.close()

    def _on_queue_declare_ok(self, _unused_frame, userdata):
        #pylint: disable=unused-argument

        prefetch_count = 1
        self._channel.basic_qos(prefetch_count=prefetch_count,
                                callback=self._on_queue_qos_ok)

    def _on_queue_qos_ok(self, _unused_frame):
        self._logger.log(LogType.Info, "Messaging | QOS for queue set")

        publishing_queue = self._settings.publishing_queues.queues
        for entry in publishing_queue:
            self._logger.log(LogType.Info, "Messaging | Creating " + \
                f"Queue '{entry.name}' | Is Durable = {entry.is_durable}")
            self._channel.queue_declare(queue=entry.name,
                                        durable=entry.is_durable)

        self._start_consuming()

    def _start_consuming(self):
        """ Setup the consumer by first calling add_on_cancel_callback so that
            the object is notified if RabbitMQ cancels the consumer. It then
            issues the Basic.Consume RPC command which returns the consumer tag
            that is used to uniquely identify the consumer with RabbitMQ. We
            keep the value to use it when we want to cancel consuming. The
            method is passed in as a callback pika will invoke when a message
            is fully received.
        """

        # Set up the consumer by first calling add_on_cancel_callback so that
        # the object is notified if RabbitMQ cancels the consumer.
        #self.add_on_cancel_callback()
        self._channel.add_on_cancel_callback(self._on_consumer_cancelled)

        self._consumer_tag = self._channel.basic_consume(
            self._settings.queue_consumer_definition.queue.name,
            self._message_processor)
        self._queue_state.was_consuming = True
        self._queue_state.is_consuming = True

    def _on_consumer_cancelled(self, method_frame):
        """ Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
            receiving messages.
        """
        self._logger.log(LogType.Info, 'Consumer was cancelled remotely, ' + \
                         f'shutting down: {method_frame}')
        if self._channel:
            self._channel.close()
            self._channel = None

    def _on_connection_open_error(self, _unused_connection, err):
        self._logger.log(LogType.Info, f'Connection open failed: {err}')
        self._reconnect()

    def _reconnect(self):
        self._queue_state.should_reconnect = True
        self.stop()

    def _on_connection_closed(self, _unused_connection, reason):

        self._channel = None
        if self._queue_state.perform_close:
            self._connection.ioloop.stop()

        else:
            msg = f": {reason.reply_text}" if reason.reply_code != 200 else ''
            self._logger.log(LogType.Info,
                             f'Connection closed, reconnect necessary {msg}')
            self._reconnect()

    def _stop_consuming(self):

        if self._channel:
            self._logger.log(LogType.Info,
                             'Stopping RabbitMQ from consuming messages')
            on_stop = functools.partial(self._on_stop_consume_ok,
                                        userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag,
                                       on_stop)

    def _on_stop_consume_ok(self, _frame, _userdata):
        self._queue_state.is_consuming = False
        self._logger.log(LogType.Info,
                         'RabbitMQ acknowledged message consumption stop')
        self._logger.log(LogType.Info, 'Closing the channel')
        self._channel.close()
