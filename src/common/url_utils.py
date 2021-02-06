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
from enum import Enum

class UrlType(Enum):
    """ Enumeration for type of URL (e.g. http or secure http) """
    http = 0
    https = 1
    unknown = 99

class UrlPrefix:
    """ Prefixes to urls such as http and https """
    #pylint: disable=too-few-public-methods

    http = 'http://'
    https = 'https://'

class UrlUtils:
    """ General utilities to use with a URL """
    #pylint: disable=too-few-public-methods

    @staticmethod
    def split_url_into_domain_and_page(url):
        """!@brief Take a full url and break it into a domain, url and type of
                   url.
        @param url URL to break into constituant pieces.
        @returns a dictionary containing the following keys: domain,  url_path,
                 url_type.  If the url prefix is unknown then domain and
                 url_path is set to None and url_type is UrlType.unknown
        """

        url_type = UrlType.unknown

        index_for_domain = -1
        if url.startswith(UrlPrefix.http):
            index_for_domain = len(UrlPrefix.http)
            url_type = UrlType.http

        elif url.startswith(UrlPrefix.https):
            index_for_domain = len(UrlPrefix.https)
            url_type = UrlType.https

        else:
            return {
                'domain': None,
                'url_path': None,
                'url_type': UrlType.unknown
            }

        domain_index = url.rfind('/', index_for_domain)

        if domain_index != -1:
            domain = url[0:domain_index]
            url_path = url[domain_index:]

        else:
            domain = url
            url_path = '/'

        return {
            'domain': domain,
            'url_path': url_path,
            'url_type': url_type
            }
