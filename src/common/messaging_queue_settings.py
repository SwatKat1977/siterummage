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

from typing import Any


class ConnectionSettings:
    ''' Messaging queue connection settings '''
    __slots__ = ['_host', '_password', '_port', '_username']

    @property
    def username(self) -> str:
        """!@brief RabbitMQ authentication Username (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._username

    @username.setter
    def username(self, value) -> None:
        """!@brief RabbitMQ username (Setter).
        @param self The object pointer.
        @param value New username.
        @returns None.
        """
        self._username = value

    @property
    def password(self) -> str:
        """!@brief RabbitMQ authentication Username password (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._password

    @password.setter
    def password(self, value) -> None:
        """!@brief RabbitMQ user password (Setter).
        @param self The object pointer.
        @param value New user password.
        @returns None.
        """
        self._password = value

    @property
    def host(self) -> str:
        """!@brief RabbitMQ host (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._host

    @host.setter
    def host(self, value) -> None:
        """!@brief RabbitMQ host (Setter).
        @param self The object pointer.
        @param value New host.
        @returns None.
        """
        self._host = value

    @property
    def port(self) -> int:
        """!@brief RabbitMQ network port (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._port

    @port.setter
    def port(self, value) -> None:
        """!@brief RabbitMQ network port (Setter).
        @param self The object pointer.
        @param value New network port.
        @returns None.
        """
        self._port = value

    def __init__(self) -> Any:
        """!@brief ConnectionSettings class constructor.
        @param self The object pointer.
        @returns Any.
        """
        self._username = 'guest'
        self._password = 'guest'
        self._host = 'localhost'
        self._port = 5672

class QueueEntry:
    ''' Definition of a queue '''
    __slots__ = ['_is_durable', '_name' ]

    @property
    def name(self) -> str:
        """!@brief RabbitMQ queue name (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._name

    @name.setter
    def name(self, value) -> None:
        """!@brief RabbitMQ queue name (Setter).
        @param self The object pointer.
        @param value New queue name.
        @returns None.
        """
        self._name = value

    @property
    def is_durable(self) -> str:
        """!@brief RabbitMQ host (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._is_durable

    @is_durable.setter
    def is_durable(self, value) -> None:
        """!@brief RabbitMQ queue is durable flag (Setter).
        @param self The object pointer.
        @param value New flag state.
        @returns None.
        """
        self._is_durable = value

    def __init__(self) -> Any:
        self._name = 'default'
        self._is_durable = False

class QueueConsumerDefinition:
    ''' Definition of the queue consumer '''
    __slots__ = ['_queue']

    @property
    def queue(self) -> QueueEntry:
        """!@brief RabbitMQ queue details (Getter).
        @param self The object pointer.
        @returns QueueEntry.
        """
        return self._queue

    def __init__(self) -> Any:
        self._queue = QueueEntry()

class PublishingQueues:
    ''' Definition of a list of queues we publish to '''
    __slots__ = ['_queues']

    @property
    def queues(self):
        return self._queues.copy()

    def __init__(self):
        self._queues = []

    def add_queue(self, queue_entry):
        self._queues.append(queue_entry)

class MessagingQueueSettings:
    ''' Messaging queue settings '''
    #__pylint: disable=too-few-public-methods
    __slots__ = ['_connection_settings', '_publishing_queues',
                 '_queue_consumer_definition']

    @property
    def connection_settings(self) -> ConnectionSettings:
        """!@brief The RabbitMQ queue connection settings (Getter).
        @param self The object pointer.
        @returns ConnectionSettings.
        """
        return self._connection_settings

    @property
    def queue_consumer_definition(self) -> QueueConsumerDefinition:
        """!@brief The RabbitMQ queue consumer definition (Getter).
        @param self The object pointer.
        @returns QueueConsumerDefinition.
        """
        return self._queue_consumer_definition

    @property
    def publishing_queues(self) -> PublishingQueues:
        """!@brief The RabbitMQ publishing queues (Getter).
        @param self The object pointer.
        @returns PublishingQueues.
        """
        return self._publishing_queues

    def __init__(self) -> Any:
        """!@brief MessagingQueueSettings class constructor.
        @param self The object pointer.
        @returns Any.
        """
        self._connection_settings = ConnectionSettings()
        self._queue_consumer_definition = QueueConsumerDefinition()
        self._publishing_queues = PublishingQueues()
