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
from typing import Any, List

class MessagingQueueSettings:
    """ Settings related to a messaging queue """
    __slots__ = ['_exchange_binding', '_exchange_routing_keys', '_is_durable',
                 '_name']
    #pylint: disable=too-few-public-methods

    @property
    def name(self) -> str:
        """!@brief Name of the message queue (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._name

    @property
    def is_durable(self) -> bool:
        """!@brief Message queue is durable flag (Getter).
        @param self The object pointer.
        @returns bool.
        """
        return self._is_durable

    @property
    def exchange_binding(self) -> str:
        """!@brief Message queue exchange binding (Getter).
        @param self The object pointer.
        @returns bool.
        """
        return self._exchange_binding

    @property
    def exchange_routing_keys(self) -> str:
        """!@brief RabbitMQ queue exchange routing keys (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._exchange_routing_keys

    def __init__(self, name, is_durable, exchange_binding,
                 exchange_routing_keys) -> Any:
        """!@brief MessagingQueueSettings constructor.
        @param self The object pointer.
        @param name Queue name.
        @param is_durable Is queue durable flag.
        @param exchange_binding Exchange the queue is bound to.
        @param exchange_routing_keys Routing keys for exchange and queue.
        @returns Any.
        """
        self._exchange_binding = exchange_binding
        self._exchange_routing_keys = exchange_routing_keys
        self._name = name
        self._is_durable = is_durable

class MessagingExchangeSettings:
    """ Settings related to a messaging exchange """
    __slots__ = ['_name', '_exchange_type']
    #pylint: disable=too-few-public-methods

    @property
    def name(self) -> str:
        """!@brief Name of the message exchange (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._name

    @property
    def exchange_type(self) -> str:
        """!@brief Type of exchange (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._exchange_type

    def __init__(self, name, exchange_type) -> Any:
        """!@brief MessagingExchangeSettings constructor.
        @param self The object pointer.
        @param name Exchange name.
        @param exchange_type Type of exchange.
        @returns Any.
        """
        self._name = name
        self._exchange_type = exchange_type

class MessagingServiceConnectSettings:
    """ Settings related to the messaging service connection """
    __slots__ = ['_username', '_password', '_host']
    #pylint: disable=too-few-public-methods

    @property
    def username(self) -> str:
        """!@brief Message service auth username (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._username

    @property
    def password(self) -> str:
        """!@brief Message service auth user password (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._password

    @property
    def host(self) -> str:
        """!@brief Message service host (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._host

    def __init__(self, username, password, host) -> Any:
        """!@brief MessagingServiceConnectSettings constructor.
        @param self The object pointer.
        @param username Authentication username.
        @param password Authentication password for user.
        @param host Message service host.
        @returns Any.
        """
        self._username = username
        self._password = password
        self._host = host

class MessagingQueueConsumerSettings:
    """ Settings related to a messaging queue consumer """
    __slots__ = ['_queue']
    #pylint: disable=too-few-public-methods

    @property
    def queue(self) -> MessagingQueueSettings:
        """!@brief Consumer queue.
        @param self The object pointer.
        @returns MessagingQueueSettings.
        """
        return self._queue

    def __init__(self, queue) -> Any:
        """!@brief MessagingQueueConsumerSettings constructor.
        @param self The object pointer.
        @param queue Instance of the queue.
        @returns Any.
        """
        self._queue = queue

class MessagingQueueProducersSettings:
    """ Settings related to a messaging queue consumer """
    __slots__ = ['_queues']
    #pylint: disable=too-few-public-methods

    @property
    def queues(self) -> List[MessagingQueueSettings]:
        """!@brief Producer queues.
        @param self The object pointer.
        @returns List of MessagingQueueSettings.
        """
        return self._queues

    def __init__(self) -> Any:
        """!@brief MessagingQueueProducersSettings constructor.
        @param self The object pointer.
        @returns Any.
        """
        self._queues = []

    def add_queue(self, new_queue : MessagingQueueSettings) ->  None:
        self._queues.append(new_queue)

class MessagingExchangesSettings:
    """ Settings related to a messaging queue exchanges """
    __slots__ = ['_exchanges']
    #pylint: disable=too-few-public-methods

    @property
    def exchanges(self) -> List[MessagingExchangeSettings]:
        """!@brief Messaging exchanges (getter).
        @param self The object pointer.
        @returns List of MessagingExchangeSettings.
        """
        return self._exchanges

    def __init__(self) -> Any:
        """!@brief MessagingExchangesSettings constructor.
        @param self The object pointer.
        @returns Any.
        """
        self._exchanges = []

    def add(self, new_exchange : MessagingExchangeSettings) ->  None:
        self._exchanges.append(new_exchange)

    def exists(self, name : str) ->  bool:
        entry = [exch for exch in self._exchanges if exch.name == name]

        return True if entry else False

class MessageQueueConfiguration:
    ''' Message queue configuration '''
    __slots__ = ['_connection_settings', '_consumer_settings',
                 '_exchanges_settings', '_producers_settings']

    @property
    def connection_settings(self) -> MessagingServiceConnectSettings:
        """!@brief Settings for the connection (Getter).
        @param self The object pointer.
        @returns MessagingServiceConnectSettings.
        """
        return self._connection_settings

    @property
    def consumer_settings(self) -> MessagingQueueConsumerSettings:
        """!@brief Settings for the consumer queue (Getter).
        @param self The object pointer.
        @returns BigBrokerApi.
        """
        return self._consumer_settings

    @property
    def producers_settings(self) -> MessagingQueueProducersSettings:
        """!@brief Settings for the producer queues (Getter).
        @param self The object pointer.
        @returns MessagingQueueProducersSettings.
        """
        return self._producers_settings

    @property
    def exchanges_settings(self) -> MessagingExchangesSettings:
        """!@brief Settings for a list of exchanges (Getter).
        @param self The object pointer.
        @returns MessagingExchangesSettings.
        """
        return self._exchanges_settings

    def __init__(self, connection_settings, consumer_settings,
                 producers_settings, exchanges_settings):
        self._connection_settings = connection_settings
        self._consumer_settings = consumer_settings
        self._producers_settings = producers_settings
        self._exchanges_settings = exchanges_settings
