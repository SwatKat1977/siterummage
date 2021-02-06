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
from time import time
from processing_queue.db_caching.cached_queue_entry import CachedQueueEntry

class UrlProcessingEntry:
    '''  Entry for a URL that is being processed'''
    __slots__ = ['_details', '_start_time']

    @property
    def details(self) -> CachedQueueEntry:
        """!@brief Cached queue entry element (Getter).
        @param self The object pointer.
        @returns CachedQueueEntry.
        """
        return self._details

    @property
    def start_time(self) -> int:
        """!@brief Time (in seconds) that url processing started (Getter).
        @param self The object pointer.
        @returns int.
        """
        return self._start_time

    def __init__(self, details, start_time) -> None:
        """!@brief UrlProcessingEntry class constructor.
        @param self The object pointer.
        @param details URL details.
        @param start_time Time (in seconds) processing started.
        @returns None.
        """
        self._details = details
        self._start_time = start_time

class UrlsBeingProcessed:
    ''' Class that handles URLs that are being processed '''
    __slots__ = ['_urls']

    def __init__(self):
        """!@brief UrlsBeingProcessed class constructor.
        @param self The object pointer.
        @returns None.
        """
        self._urls = {}

    def url_being_processed(self, url) -> bool:
        """!@brief Check to see if a url is already being processed.
        @param self The object pointer.
        @param url URL to check.
        @returns Being processed boolean (True = being processed).
        """

        return url in self._urls

    def add_url(self, url_details) -> None:
        """!@brief Add a neq url specified in the parameter, if it already
                   exists then it's not added.
        @param self The object pointer.
        @param url_details URL details.
        @returns None.
        """

        if url_details.url in self._urls:
            return

        entry = UrlProcessingEntry(url_details, round(time()))
        self._urls[url_details.url] = entry

    def get_url(self, url):
        """!@brief Get a url specified in the parameter, if it cannot be found
                   then None is returned.
        @param self The object pointer.
        @param url URL string.
        @returns URL details or None if not found.
        """

        try:
            return self._urls[url]

        except KeyError:
            return None
