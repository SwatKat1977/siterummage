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

class BigBrokerApi:
    """ Settings related to the Big Broker Api """
    __slots__ = ['_api_endpoint', '_auth_key']

    @property
    def api_endpoint(self) -> str:
        """!@brief API endpoint (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._api_endpoint

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    def __init__(self, auth_key, api_endpoint):
        self._auth_key = auth_key
        self._api_endpoint = api_endpoint

class PageStoreApi:
    """ Settings related to the Page Store Api """
    __slots__ = ['_api_endpoint', '_auth_key']

    @property
    def api_endpoint(self) -> str:
        """!@brief API endpoint (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._api_endpoint

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    def __init__(self, auth_key, api_endpoint):
        self._auth_key = auth_key
        self._api_endpoint = api_endpoint

class ProcessingQueueApi:
    """ Settings related to the Processing Queue Api """
    __slots__ = ['_api_endpoint', '_auth_key']

    @property
    def api_endpoint(self) -> str:
        """!@brief API endpoint (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._api_endpoint

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    def __init__(self, auth_key, api_endpoint):
        self._auth_key = auth_key
        self._api_endpoint = api_endpoint

class ApiSettings:
    """ Settings related to own Api """
    __slots__ = ['_auth_key', '_public_key_file']

    @property
    def auth_key(self) -> str:
        """!@brief Auth key for the Api (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._auth_key

    @property
    def public_key_file(self) -> str:
        """!@brief Public key filename (Getter).
        @param self The object pointer.
        @returns string.
        """
        return self._public_key_file

    def __init__(self, auth_key, public_key_file):
        self._auth_key = auth_key
        self._public_key_file = public_key_file

class Configuration:
    ''' Scrape Node configuration '''
    __slots__ = ['_api_settings', '_big_broker_api', '_page_store_api',
                 '_processing_queue_api']

    @property
    def api_settings(self) -> ApiSettings:
        """!@brief Settings for own Api settings (Getter).
        @param self The object pointer.
        @returns ApiSettings.
        """
        return self._api_settings

    @property
    def big_broker_api(self) -> BigBrokerApi:
        """!@brief Settings for the Big Broker Api (Getter).
        @param self The object pointer.
        @returns BigBrokerApi.
        """
        return self._big_broker_api

    @property
    def page_store_api(self) -> PageStoreApi:
        """!@brief Settings for the Page Store Api (Getter).
        @param self The object pointer.
        @returns PageStoreApi.
        """
        return self._page_store_api

    @property
    def processing_queue_api(self) -> ProcessingQueueApi:
        """!@brief Settings for the Processing Queue Api (Getter).
        @param self The object pointer.
        @returns ProcessingQueueApi.
        """
        return self._processing_queue_api

    def __init__(self, api_settings, big_broker_api, page_store_api,
                 processing_queue_api):
        self._api_settings = api_settings
        self._big_broker_api = big_broker_api
        self._page_store_api = page_store_api
        self._processing_queue_api = processing_queue_api
