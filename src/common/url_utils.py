'''
Copyright (C) 2021 Siterummage
All Rights Reserved.

NOTICE:  All information contained herein is, and remains the property of
Siterummage.  The intellectual and technical concepts contained herein are
proprietary to Siterummage and may be covered by U.K. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from Siterummage.
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
