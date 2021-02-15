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

class ScrapedPage:
    ''' Class that encapsulate the data for a scraped page '''
    __slots__ = ['_description', '_domain', '_page_hash', '_title',
                 '_url_path']

    @property
    def description(self) -> str:
        """!@brief Description of webpage (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._description

    @property
    def domain(self) -> str:
        """!@brief Domain part of the webpage (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._domain

    @property
    def page_hash(self) -> str:
        """!@brief Hash of the scraped webpage (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._page_hash

    @property
    def title(self) -> str:
        """!@brief Title of the webpage (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._title

    @property
    def url_path(self) -> str:
        """!@brief The URL part of the webpage (Getter).
        @param self The object pointer.
        @returns str.
        """
        return self._url_path

    def __init__(self, description, domain, page_hash, title, url_path):
        """!@brief ScrapedPage data class constructor.
        @param self The object pointer.
        @param description Description of webpage .
        @param domain Domain name part of URL.
        @param page_hash Hash of the scraped webpage.
        @param title Title of the webpage.
        @param url_path The URL part of the webpage.
        @returns self.
        """
        #pylint: disable=too-many-arguments
        self._description = description
        self._domain = domain
        self._page_hash = page_hash
        self._title = title
        self._url_path = url_path
