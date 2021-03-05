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
from scraped_page import ScrapedPage

class ScrapedPageBuilder:
    """ Class for building a ScrapedPage object """
    __slots__ = ['_description', '_domain', '_hash', '_title', '_url_path']

    def set_description(self, value) -> object:
        """!@brief Set description parameter for page builder.
        @param self The object pointer.
        @param self New description.
        @returns instance of ScrapedPage with description set.
        """
        self._description = value
        return self

    def set_domain(self, value):
        """!@brief Set domain parameter for page builder.
        @param self The object pointer.
        @param self New domain.
        @returns instance of ScrapedPage with domain set.
        """
        self._domain = value
        return self

    def set_hash(self, value):
        """!@brief Set page hash for page builder.
        @param self The object pointer.
        @param self New hash for page contents.
        @returns instance of ScrapedPage with page hash set.
        """
        self._hash = value
        return self

    def set_title(self, value):
        """!@brief Set page title for page builder.
        @param self The object pointer.
        @param self New title for page contents.
        @returns instance of ScrapedPage with page title set.
        """
        self._title = value
        return self

    def set_url_path(self, value):
        """!@brief Set page url path for page builder.
        @param self The object pointer.
        @param self New page url path.
        @returns instance of ScrapedPage with page url path set.
        """
        self._url_path = value
        return self

    def __init__(self):
        self._description = ''
        self._domain = None
        self._hash = None
        self._title = ''
        self._url_path = None

    def build(self) -> ScrapedPage:
        """!@brief Build a ScrapedPage object, after validating the fields
                   passed to the builder.  On falure an AttributeError
                   exception is raised.
        @param self The object pointer.
        @returns ScrapedPage or exception if validation failure.
        """

        if not self._domain:
            raise AttributeError('Missing domain attribute')

        if not self._hash:
            raise AttributeError('Missing hash attribute')

        if not self._url_path:
            raise AttributeError('Missing url path attribute')

        return ScrapedPage(self._description, self._domain,  self._hash,
                           self._title, self._url_path)

    def reset(self) -> None:
        """!@brief Reset the builder properies back to default.
        @param self The object pointer.
        @returns None.
        """

        self._description = ''
        self._domain = None
        self._hash = None
        self._title = ''
        self._url_path = None
